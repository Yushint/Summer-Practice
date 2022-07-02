from flask import Flask, url_for, render_template, request, flash, redirect
from database import DB
from models import UsersModel
from werkzeug.security import generate_password_hash, check_password_hash


db = DB()
UsersModel(db.get_connection()).initialize_table()
app = Flask(__name__)
app.config["SECRET_KEY"] = "summer_practice_secret_key" # защита cookies

@app.route("/welcome_page")
def welcome_page_handler():
    pass

@app.route("/game_news")
def game_news_page_handler():
    pass

@app.route("/")
@app.route("/user_data_forms")
def user_data_forms():
    return render_template("index.html")

@app.route("/user_authorization_handler", methods=["GET", "POST"])
def user_authorization_handler():
    if request.method == "POST":
        return request.form

@app.route("/user_registration_handler", methods=["GET", "POST"])
def user_registration_handler():
    if request.method == "POST":
        user_name = request.form["reg-username"]
        password_hash = generate_password_hash(request.form["reg-userpass"], "sha256")
        email = request.form["reg-usermail"]
        users_model = UsersModel(db.get_connection())
        if user_name in [user[1] for user in users_model.get_all_users()]:
            message = "Ошибка. Пользователь с таким именем уже существует."
            return render_template("index.html", error_message=message)
        else:
            users_model.insert(user_name, password_hash, email)
            return "Ok" # redirect(url_for(...))
        #session['_flashes'].clear()
        #return redirect(url_for("user_data_forms"))

@app.route("/about_us")
def about_us_page_handler():
    pass

@app.route("/administrator")
def administrator_page_handler():
    pass

if __name__ == "__main__":
    app.run(debug=True, port=8080)
