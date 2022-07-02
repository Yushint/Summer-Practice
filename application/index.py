from flask import Flask, url_for, render_template, request

app = Flask(__name__)

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
        return request.form

@app.route("/about_us")
def about_us_page_handler():
    pass

@app.route("/administrator")
def administrator_page_handler():
    pass

if __name__ == "__main__":
    app.run(debug=True, port=8080)
