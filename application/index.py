from flask import Flask

app = Flask(__name__)

@app.route("/welcome_page")
def welcome_page_handler():
    pass

@app.route("/game_news")
def game_news_page_handler():
    pass

@app.route("/authorization")
def authorization_page_handler():
    pass

@app.route("/registration")
def registration_page_handler():
    pass

@app.route("/about_us")
def about_us_page_handler():
    pass

@app.route("/administrator")
def administrator_page_handler():
    pass

if __name__ == "__main__":
    app.run(debug=True, port=8080)