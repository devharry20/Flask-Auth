import os

import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login.login_manager import LoginManager
from oauthlib.oauth2 import WebApplicationClient


db = SQLAlchemy()
DB_NAME = os.getcwd() + r"\database.db"

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

def get_google_provider_cfg():
    """A function to gather data used for Google authentication"""
    return requests.get(GOOGLE_DISCOVERY_URL).json()

def create_app():
    """Main function to run Flask app and set config"""
    app = Flask(__name__, template_folder=os.getcwd() + r"\app\pages")
    app.config["SECRET_KEY"] = "abc123"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    global client
    client = WebApplicationClient(GOOGLE_CLIENT_ID)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app