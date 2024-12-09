from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os

APP = Flask(__name__)
SOCKET = SocketIO(APP)

ALL_METHODS = ['GET', 'POST']


def init_app():
    load_dotenv()

    APP.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    APP.config['SERVER_NAME'] = os.getenv('SERVER_NAME')
    APP.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    from .views import views
    from .auth import auth

    APP.register_blueprint(views, url_prefix='/')
    APP.register_blueprint(auth, url_prefix='/')

    from .mailservice import start
    start()

    #from .temporary import start_updater
    #start_updater()
