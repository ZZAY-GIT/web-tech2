from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
import re
from functools import wraps
from sqlalchemy import func
from datetime import datetime
import os
from io import StringIO
import csv
from flask import Response


app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-super-secret-12345')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@app.before_request
def log_visit():
    if request.path.startswith('/static') or request.path == '/favicon.ico':
        return

    user_id = current_user.id if current_user.is_authenticated else None

    visit = VisitLog(
        path=request.full_path,
        user_id=user_id
    )
    db.session.add(visit)
    db.session.commit()


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(100))
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref='users')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class VisitLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', backref='visits', lazy=True)


def check_rights(action):
    """ action: 'create', 'edit_any', 'delete', 'view_any_profile', 'view_all_logs', 'edit_own', 'view_own_logs' """
    def decorator(view_func):
        @wraps(view_func)
        def decorated(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Необходимо войти в систему', 'warning')
                return redirect(url_for('login'))

            role = current_user.role.name if current_user.role else 'guest'

            allowed = False

            if role == 'admin':
                allowed = True
            elif role == 'user':
                if action in ['edit_own', 'view_own_logs', 'view_own_profile']:
                    allowed = True
                elif action == 'view_profile' and 'id' in kwargs and kwargs['id'] == current_user.id:
                    allowed = True

            if not allowed:
                flash('У вас недостаточно прав для доступа к данной странице.', 'danger')
                return redirect(url_for('index'))

            return view_func(*args, **kwargs)
        return decorated
    return decorator



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

def strong_password_check(form, field):
    p = field.data
    if not p:
        raise ValidationError("Пароль обязателен")
    if len(p) < 8 or len(p) > 128:
        raise ValidationError("Пароль должен быть от 8 до 128 символов")
    if not re.search(r'[A-Z]', p):
        raise ValidationError("Нужна хотя бы одна заглавная буква")
    if not re.search(r'[a-zа-я]', p):
        raise ValidationError("Нужна хотя бы одна строчная буква")
    if not re.search(r'\d', p):
        raise ValidationError("Нужна хотя бы одна цифра")
    if ' ' in p:
        raise ValidationError("Пробелы запрещены")
    allowed = r'^[a-zA-Zа-яА-Я0-9~!?@#$%^&*()_\-+=\[\]{}><\\/|"\':;.,]+$'
    if not re.match(allowed, p):
        raise ValidationError("Недопустимые символы")

class UserCreateForm(FlaskForm):
    login = StringField('Логин', validators=[
        DataRequired(), Length(min=5, max=50),
        lambda f, field: ValidationError("Только латинские буквы и цифры")
            if not re.match(r'^[a-zA-Z0-9]+$', field.data) else None
    ])
    password = PasswordField('Пароль', validators=[DataRequired(), strong_password_check])
    last_name   = StringField('Фамилия')
    first_name  = StringField('Имя', validators=[DataRequired()])
    middle_name = StringField('Отчество')
    role_id     = SelectField('Роль', coerce=int)
    submit      = SubmitField('Сохранить')

class UserEditForm(UserCreateForm):
    login = None
    password = None

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Старый пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired(), strong_password_check])
    new_password2 = PasswordField('Повторите новый пароль', validators=[
        DataRequired(), EqualTo('new_password', message='Пароли не совпадают')
    ])
    submit = SubmitField('Сменить пароль')


def get_fio(user):
    parts = [user.last_name or '', user.first_name, user.middle_name or '']
    return ' '.join(filter(None, parts)).strip() or user.login


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users, get_fio=get_fio)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Неверный логин или пароль', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<int:id>')
def user_view(id):
    user = User.query.get_or_404(id)
    if current_user.role and current_user.role.name == 'admin' or user.id == current_user.id:
        return render_template('user_view.html', user=user, get_fio=get_fio)
    flash('У вас недостаточно прав', 'danger')
    return redirect(url_for('index'))

@app.route('/user/create', methods=['GET', 'POST'])
@login_required
@check_rights('create')
def user_create():
    form = UserCreateForm()
    form.role_id.choices = [(0, '— без роли —')] + [(r.id, r.name) for r in Role.query.all()]
    if form.validate_on_submit():
        if User.query.filter_by(login=form.login.data).first():
            flash('Такой логин уже занят', 'danger')
            return render_template('user_form.html', form=form, title='Создание пользователя')
        user = User(
            login=form.login.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data or None,
            middle_name=form.middle_name.data or None,
            role_id=form.role_id.data if form.role_id.data != 0 else None
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Пользователь создан', 'success')
        return redirect(url_for('index'))
    return render_template('user_form.html', form=form, title='Создание пользователя')

@app.route('/user/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def user_edit(id):
    user = User.query.get_or_404(id)
    if current_user.role.name == 'admin':
        allowed = True
    elif current_user.id == user.id:
        allowed = True
    else:
        allowed = False
    if not allowed:
        flash('У вас недостаточно прав для редактирования этого пользователя', 'danger')
        return redirect(url_for('index'))
    
    form = UserEditForm(obj=user)
    form.role_id.choices = [(0, '— без роли —')] + [(r.id, r.name) for r in Role.query.all()]
    form.role_id.data = user.role_id or 0

    if current_user.role.name != 'admin':
        form.role_id.render_kw = {'disabled': 'disabled'}

    if form.validate_on_submit():
        user.first_name  = form.first_name.data
        user.last_name   = form.last_name.data or None
        user.middle_name = form.middle_name.data or None

        if current_user.role.name == 'admin':
            user.role_id = form.role_id.data if form.role_id.data != 0 else None

        db.session.commit()
        flash('Данные обновлены', 'success')
        return redirect(url_for('index'))
    return render_template('user_form.html', form=form, title='Редактирование пользователя', user=user)


@app.route('/user/<int:id>/delete', methods=['POST'])
@login_required
@check_rights('delete')
def user_delete(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('Нельзя удалить самого себя', 'danger')
        return redirect(url_for('index'))
    db.session.delete(user)
    db.session.commit()
    flash('Пользователь удалён', 'success')
    return redirect(url_for('index'))

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Неверный старый пароль', 'danger')
            return render_template('change_password.html', form=form)
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Пароль изменён', 'success')
        return redirect(url_for('index'))
    return render_template('change_password.html', form=form)


def init_db():
    with app.app_context():
        db.create_all()
        if Role.query.count() == 0:
            roles = [
                Role(name='admin', description='Администратор'),
                Role(name='user', description='Обычный пользователь'),
            ]
            db.session.bulk_save_objects(roles)
            db.session.commit()

        if User.query.count() == 0:
            admin = User(
                login='admin',
                first_name='Админ',
                last_name='Администратор',
                middle_name='Тестовый',
                role_id=Role.query.filter_by(name='admin').first().id
            )
            admin.set_password('Admin123!')
            
            db.session.add(admin)
            db.session.commit()
            print("Создан тестовый администратор: login='admin', пароль='Admin123!'")


@app.route('/visit-logs')
@login_required
def visit_logs():
    if current_user.role.name != 'admin':
        return redirect(url_for('my_visit_logs'))

    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    pagination = VisitLog.query.order_by(VisitLog.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('visit_logs.html', 
                          visits=pagination.items, 
                          pagination=pagination,
                          get_fio=get_fio,
                          is_admin=True)


@app.route('/visit-logs/my')
@login_required
@check_rights('view_own_logs')
def my_visit_logs():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    pagination = VisitLog.query.filter_by(user_id=current_user.id)\
        .order_by(VisitLog.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('visit_logs.html', 
                          visits=pagination.items, 
                          pagination=pagination,
                          get_fio=get_fio,
                          is_my=True)


@app.route('/reports/pages')
@login_required
@check_rights('view_all_logs')
def report_pages():
    stats = db.session.query(
        VisitLog.path,
        func.count(VisitLog.id).label('visits')
    ).group_by(VisitLog.path)\
     .order_by(func.count(VisitLog.id).desc())\
     .all()
    
    return render_template('report_pages.html', stats=stats)


@app.route('/reports/users')
@login_required
@check_rights('view_all_logs')
def report_users():
    subq = db.session.query(
        VisitLog.user_id,
        func.count(VisitLog.id).label('visits')
    ).group_by(VisitLog.user_id)\
     .subquery()
    
    stats = db.session.query(subq.c.user_id, subq.c.visits)\
        .order_by(subq.c.visits.desc())\
        .all()
    
    result = []
    for user_id, cnt in stats:
        if user_id:
            u = User.query.get(user_id)
            name = get_fio(u) if u else "— удалён —"
        else:
            name = "Неавторизованный пользователь"
        result.append((name, cnt))
    
    return render_template('report_users.html', stats=result)


@app.route('/reports/users/export')
@login_required
@check_rights('view_all_logs')
def export_users():
    subq = db.session.query(
        VisitLog.user_id,
        func.count(VisitLog.id).label('visits')
    ).group_by(VisitLog.user_id)\
     .subquery()
    
    stats = db.session.query(subq.c.user_id, subq.c.visits)\
        .order_by(subq.c.visits.desc())\
        .all()
    
    result = []
    for user_id, cnt in stats:
        if user_id:
            u = db.session.get(User, user_id)
            name = get_fio(u) if u else "— удалён —"
        else:
            name = "Неаутентифицированный пользователь"
        result.append((name, cnt))
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Пользователь', 'Посещений'])
    
    for name, count in result:
        writer.writerow([name, count])
    
    response = Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=users_report.csv"}
    )
    return response


if __name__ == '__main__':
    init_db()
    app.run(debug=True)