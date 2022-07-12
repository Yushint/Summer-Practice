# -*- coding: utf-8 -*-

import os
import datetime
from flask import Flask, url_for, render_template, request, flash, redirect, session, abort
from database import DB
from models import UsersModel, ArticlesModel, SelectedArticlesModel
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from AdministratorNewsletterHandler import AdministratorNewsletter


db = DB()
UsersModel(db.get_connection()).initialize_table()
ArticlesModel(db.get_connection()).initialize_table()
SelectedArticlesModel(db.get_connection()).initialize_table()


IMAGE_FOLDER = './static/img'
ALLOWED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def is_file_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


app = Flask(__name__)
app.config["SECRET_KEY"] = "summer_practice_secret_key" # защита cookies и session
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
app.permanent_session_lifetime = datetime.timedelta(days=5)


@app.route("/logout")
def logout():
    """Обработчика выхода из системы."""
    session.clear()
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
        remember_me = True if request.form.get("auth-remember_pass") else False
        users_model = UsersModel(db.get_connection())
        if users_model.is_user_exists(user_name)[0] and check_password_hash(users_model.is_user_exists(user_name)[1], user_password):
            session["username"] = user_name
            session["userid"] = users_model.get_user_id(user_name)
            session["usermail"] = users_model.get_user(session["userid"])[3]
            if remember_me:
                session.permanent = True
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
    return render_template("home.html", articles=articles_list, title="GameNews - Статьи")

@app.route("/profile/<string:username>")
def profile_page(username):
    """ Обработчик страницы профиля пользователя. """
    if "username" not in session:
        return redirect(url_for("user_data_handler"))
    users_model = UsersModel(db.get_connection())
    selected_articles_model = SelectedArticlesModel(db.get_connection())
    articles_model = ArticlesModel(db.get_connection())
    if users_model.is_user_exists(username)[0]:
        if session["username"] != username:
            abort(401)        
        user_id = users_model.get_user_id(username)
        user_info = users_model.get_user(user_id)
        selected_articles_list = selected_articles_model.get_selected_articles_id(user_id)
        articles = []
        for element in selected_articles_list:
            articles.append(articles_model.get_article(element))
            #user_name[1], password_hash[2], email[3], is_admin[4], avatar[5] 
        return render_template("profile.html", articles=articles, user=user_info) # render_template("profile")
    else:
        abort(404)
        
@app.route("/avatar_changing", methods=["GET", "POST"])
def profile_avatar_changing():
    if "username" not in session:
        return redirect(url_for("user_data_handler"))
    if request.method == "POST":
        profile_avatar = request.files["user_avatar"]
        if is_file_allowed(profile_avatar.filename):
            filename = secure_filename(profile_avatar.filename)
            avatar_link = os.path.join(app.config['IMAGE_FOLDER'], filename)
            profile_avatar.save(avatar_link)
        else:
            flash("Выберите файл(ы) формата png, jpg или jpeg.", "error")
            return redirect(url_for("profile_page", username=session["username"]))
        avatar_link = '.' + avatar_link
        users_model = UsersModel(db.get_connection())
        user_id = users_model.get_user_id(session["username"])
        users_model.set_avatar(user_id, avatar_link)
        flash("Аватар успешно изменён.", "success")
    return redirect(url_for("profile_page", username=session["username"]))
        
    
@app.route("/article/select_article/<int:selection_id>", methods=["GET", "POST"])
def article_selection_handler(selection_id):
    """ Обработчки добавления статьи в избранное."""
    if request.method == "POST":
        selected_articles_model = SelectedArticlesModel(db.get_connection())
        users_model = UsersModel(db.get_connection())
        if selected_articles_model.is_selected_article_exists(users_model.get_user_id(session["username"]), selection_id)[0]:
            flash("Статья в избранном.", "success")
        else:
            selected_articles_model.insert(users_model.get_user_id(session["username"]), selection_id)
            flash("Статья в избранном.", "success")
    return redirect(url_for("article_page", article_id=selection_id))

@app.route("/article/<int:article_id>")
def article_page(article_id):
    """Обработчик страницы конкретной статьи."""
    if "username" not in session:
        return redirect(url_for("user_data_handler"))
    articles_model = ArticlesModel(db.get_connection())
    if articles_model.is_article_exists(article_id)[0]:
        current_article = articles_model.get_article(article_id)
        return render_template("page.html", article=current_article) # позже берём статью по уникальному id или url и рендерим.
    else:
        abort(404) #sqlite3 exception.
        #id[0] author[1] title[2] key_theme[3] text[4] image_preview[5] image_top[6] image_bottom[7]
    
@app.route("/administrator")
def administrator_page():
    """Обработка страницы администратора."""
    if "username" not in session:
        return redirect(url_for("user_data_handler"))
    elif session["username"] != "admin":
        abort(401)
    else:
        return render_template("admin.html")
    
@app.route("/administrator/add_article", methods=["GET", "POST"])
def admin_add_article():
    """ Обработчик добавления новой статьи администратором. """
    if "username" not in session:
        return redirect(url_for("user_data_handler"))
    elif session["username"] != "admin":
        abort(401)
    else:
        if request.method == "POST":
            article_author = request.form["article_author"]
            article_title = request.form["article_title"]
            article_key_theme = request.form["article_key_theme"]
            article_text = request.form["article_text"]
            article_preview_image = request.files["article_preview_image"]
            article_header_image = request.files["article_header_image"]
            article_bottom_image = request.files["article_bottom_image"]
            if is_file_allowed(article_preview_image.filename):
                filename = secure_filename(article_preview_image.filename)
                preview_link = os.path.join(app.config['IMAGE_FOLDER'], filename)
                article_preview_image.save(preview_link)
            else:
                flash("Выберите файл(ы) формата png, jpg или jpeg.", "error")
                return redirect(url_for("administrator_page"))
            if is_file_allowed(article_header_image.filename):
                filename = secure_filename(article_header_image.filename)
                header_link = os.path.join(app.config['IMAGE_FOLDER'], filename)
                article_header_image.save(header_link)
            else:
                flash("Выберите файл(ы) формата png, jpg или jpeg.", "error")
                return redirect(url_for("administrator_page"))
            if is_file_allowed(article_bottom_image.filename):
                filename = secure_filename(article_bottom_image.filename)
                bottom_link = os.path.join(app.config['IMAGE_FOLDER'], filename)
                article_bottom_image.save(bottom_link)
            else:
                flash("Выберите файл(ы) формата png, jpg или jpeg.", "error")
                return redirect(url_for("administrator_page"))
            preview_link = '.' + preview_link
            header_link = '.' + header_link
            bottom_link = '.' + bottom_link
            articles_model = ArticlesModel(db.get_connection())
            articles_model.insert(article_author, article_title, article_key_theme, article_text,
                                  preview_link, header_link, bottom_link)
            flash("Статья успешно добавлена.", "success")
    return redirect(url_for("administrator_page"))

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
