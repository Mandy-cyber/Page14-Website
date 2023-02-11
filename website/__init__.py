from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "love.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'somesecretkeywillgohereanddontforgettowritean.envfile' # TODO change this secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
 
    from .models import User, Matches, BookQuotes
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #where the website should direct us if the user is not logged in
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) #get knows tht we are looking for id

    return app


def create_database(app): #check if database already exists. if not, create it
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")
