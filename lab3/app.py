from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "super-secret-key-ChangeMeInProduction2026"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Пожалуйста, войдите, чтобы получить доступ к этой странице."
login_manager.login_message_category = "warning"


class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash


users = {
    "user": User(
        id="1",
        username="user",
        password_hash=generate_password_hash("qwerty")
    )
}


@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == user_id:
            return user
    return None


@app.route("/")
def index():
    if "visit_count" not in session:
        session["visit_count"] = 1
    else:
        session["visit_count"] += 1

    visit_count = session["visit_count"]

    message = None
    if current_user.is_authenticated:
        message = f"Вы успешно вошли как {current_user.username}"

    return render_template(
        "index.html",
        visit_count=visit_count,
        message=message
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        user = users.get(username)

        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=remember)
            flash("Вы успешно вошли", "success")
            next_page = request.args.get("next")
            if next_page and next_page.startswith("/"):
                return redirect(next_page)
            return redirect(url_for("index"))
        else:
            flash("Неверное имя пользователя или пароль", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из системы", "info")
    return redirect(url_for("index"))


@app.route("/secret")
@login_required
def secret():
    return render_template("secret.html")


if __name__ == "__main__":
    app.run(debug=True)