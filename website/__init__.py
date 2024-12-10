from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
from pathlib import Path
import os

APP = Flask(__name__)
SOCKET = SocketIO(APP, async_mode='eventlet')

ALL_METHODS = ['GET', 'POST']


def init_app():
    env_path = Path(__file__).resolve().parent.parent / 'server.env'
    load_dotenv(dotenv_path=env_path)

    APP.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    APP.config['SERVER_NAME'] = os.getenv('SERVER_NAME')
    APP.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    from .views import views
    from .auth import auth

    APP.register_blueprint(views, url_prefix='/')
    APP.register_blueprint(auth, url_prefix='/')

    from .logic import socket

    from .mailservice import start
    start()

    if os.getenv('EXEC_MODE') != 'DEBUG':
        from .temporary import start_updater
        start_updater()
