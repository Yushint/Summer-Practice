from flask import Flask, url_for, render_template, request, flash, redirect, session
from database import DB
from models import UsersModel
from werkzeug.security import generate_password_hash, check_password_hash


db = DB()
UsersModel(db.get_connection()).initialize_table()
app = Flask(__name__)
app.config["SECRET_KEY"] = "summer_practice_secret_key" # защита cookies


@app.route("/logout")
def logout():
    """Обработчика выхода из системы."""
    session.pop("username", 0)
    return redirect(url_for("user_data_forms"))

@app.route("/user_authorization_handler", methods=["GET", "POST"])
def user_authorization_handler():
    """Обработка запроса на авторизацию."""
    if request.method == "POST":
        user_name = request.form["auth-username"]
        user_password = request.form["auth-userpass"]
        users_model = UsersModel(db.get_connection())
        if users_model.is_user_exists(user_name)[0] and check_password_hash(users_model.is_user_exists(user_name)[1], user_password):
            session["username"] = user_name
            return (user_name) #redirect(url_for(...))
        else:
            flash("Пользователь или пароль неверны.")
    return redirect(url_for("user_data_forms"))
        

@app.route("/user_registration_handler", methods=["GET", "POST"])
def user_registration_handler():
    """Обработка запроса на регистрацию."""
    if request.method == "POST":
        user_name = request.form["reg-username"]
        password_hash = generate_password_hash(request.form["reg-userpass"], "sha256")
        email = request.form["reg-usermail"]
        users_model = UsersModel(db.get_connection())
        if user_name in [user[1] for user in users_model.get_all_users()]:
            flash("Ошибка. Пользователь с таким именем уже существует.")
        else:
            users_model.insert(user_name, password_hash, email)
            return "Ok" # redirect(url_for(...))
    return redirect(url_for("user_data_forms"))

@app.route("/game_news")
def game_news_page_handler():
    """Обработчик главной страницы."""
    pass

@app.route("/")
@app.route("/user_data_forms")
def user_data_forms():
    """Обработчик страницы форм регистрации/авторизации."""
    return render_template("index.html", title="Регистрация пользователя.")
        
@app.route("/about_us")
def about_us_page_handler():
    """Обработка страницы "О нас" """
    pass

@app.route("/administrator")
def administrator_page_handler():
    """Обработка страницы администратора."""
    pass

if __name__ == "__main__":
    app.run(debug=True, port=8080)
