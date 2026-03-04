from flask import Flask, render_template, request
import re

app = Flask(__name__)
application = app


@app.route("/")
def start():
    return render_template("base.html")


@app.route("/info", methods=["GET", "POST"])
def info():
    info = {
        "args": dict(request.args),
        "headers": dict(request.headers),
        "cookies": dict(request.cookies),
        "form": dict(request.form)
    }
    return render_template("info.html", info=info)


@app.route("/phone", methods=["GET", "POST"])
def check_phone():
    error = None
    formatted = None
    phone_value = ""

    if request.method == "POST":
        phone = request.form.get("phone", "").strip()
        phone_value = phone

        if not phone:
            error = "Введите номер телефона"
        else:
            digits = re.sub(r"[^0-9]", "", phone)

            starts_with_plus7_or_8 = phone.lstrip().startswith(("+7", "8"))
            expected_length = 11 if starts_with_plus7_or_8 else 10

            if len(digits) != expected_length:
                error = "Недопустимый ввод. Неверное количество цифр."
            else:
                if not re.match(r'^[\d\s().+-]+$', phone):
                    error = "Недопустимый ввод. В номере телефона встречаются недопустимые символы."
                else:
                    if digits.startswith("7") and len(digits) == 11:
                        digits = "8" + digits[1:]
                    elif digits.startswith("8") and len(digits) == 11:
                        pass
                    elif len(digits) == 10:
                        digits = "8" + digits

                    formatted = (
                        digits[0] + "-" +
                        digits[1:4] + "-" +
                        digits[4:7] + "-" +
                        digits[7:9] + "-" +
                        digits[9:11]
                    )

    return render_template(
        "phone.html",
        error=error,
        formatted=formatted,
        phone_value=phone_value
    )

if __name__ == "__main__":
    app.run(debug=True)