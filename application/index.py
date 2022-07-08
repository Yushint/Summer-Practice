# -*- coding: utf-8 -*-

from flask import Flask, url_for, render_template, request, flash, redirect, session, abort
from database import DB
from models import UsersModel, ArticlesModel
from werkzeug.security import generate_password_hash, check_password_hash
from AdministratorNewsletterHandler import AdministratorNewsletter


db = DB()
UsersModel(db.get_connection()).initialize_table()
ArticlesModel(db.get_connection()).initialize_table()

app = Flask(__name__)
app.config["SECRET_KEY"] = "summer_practice_secret_key" # защита cookies и session


@app.route("/logout")
def logout():
    """Обработчика выхода из системы."""
    session.pop("username", 0)
    return redirect(url_for("user_data_handler"))

@app.route("/user_data_forms")
@app.route("/")
def user_data_handler():
    """Обработчик страницы форм регистрации/авторизации."""
    if "username" in session:
        return redirect(url_for("main_page"))
    return render_template("index.html", title="GameNews - Авторизация.")

@app.route("/user_authorization_handler", methods=["GET", "POST"])
def user_authorization_handler():
    """Обработка запроса на авторизацию."""
    if "username" in session:
        return redirect(url_for("main_page"))
    if request.method == "POST":
        user_name = request.form["auth-username"]
        user_password = request.form["auth-userpass"]
        users_model = UsersModel(db.get_connection())
        if users_model.is_user_exists(user_name)[0] and check_password_hash(users_model.is_user_exists(user_name)[1], user_password):
            session["username"] = user_name
            return redirect(url_for("main_page"))
        else:
            flash("Пользователь или пароль неверны.")
    return render_template("index.html", title="Регистрация и авторизация пользователя.")
        

@app.route("/user_registration_handler", methods=["GET", "POST"])
def user_registration_handler():
    if "username" in session:
        return redirect(url_for("main_page"))   
    """Обработка запроса на регистрацию."""
    if request.method == "POST":
        user_name = request.form["reg-username"]
        user_password = request.form["reg-userpass"]
        user_email = request.form["reg-usermail"]
        password_hash = generate_password_hash(user_password, "sha256")
        users_model = UsersModel(db.get_connection())
        if user_name in [user[1] for user in users_model.get_all_users()]:
            flash("Ошибка. Пользователь с таким именем уже существует.")
        else:
            try:
                email_title="Благодарим за регистрацию на сайте GameNews!"
                email_text=f"""Ваш username: {user_name}.\nВаш пароль: {user_password}."""
                admin_newsletter = AdministratorNewsletter(email_title, email_text)
                admin_newsletter.define_newsletter_message()
                admin_newsletter.send_newsletter_message([user_email])
            except Exception:
                pass
            users_model.insert(user_name, password_hash, user_email)
            session["username"] = user_name
            return redirect(url_for("main_page"))
    return render_template("index.html", title="Регистрация и авторизация пользователя.")

@app.route("/game_news")
def main_page():
    """Обработчик главной страницы."""
    if "username" not in session:
        return redirect(url_for("user_data_handler"))
    articles_model = ArticlesModel(db.get_connection())
    articles_list = articles_model.get_all_articles(amount=5)
    #id[0] author[1] title[2] key_theme[3] text[4] image[5]
    return render_template("home.html", articles=articles_list, title="GameNews - Статьи")

@app.route("/article/<int:article_id>")
def article_page(article_id):
    """Обработчик страницы конкретной статьи."""
    if "username" not in session:
        return redirect(url_for("user_data_handler"))
    articles_model = ArticlesModel(db.get_connection())
    current_article = articles_model.get_article(article_id)
    return render_template("page1.html", article=current_article) # позже берём статью по уникальному id или url и рендерим.
        
@app.route("/administrator")
def administrator_page():
    """Обработка страницы администратора."""
    if "username" not in session:
        return redirect(url_for("user_data_handler"))
    elif "username" != "admin":
        abort(401)
    else:
        return "Administrator Page"

@app.errorhandler(404)
def error_404_page(error):
    """Обработчик ошибки 404.
       Отсутствие запрашиваемой страницы."""
    return render_template("error_404.html")

@app.errorhandler(401)
def error_401_page(error):
    """Обработчик ошибки 401.
       Отказ в доступности.
    """
    return render_template("error_401.html")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
