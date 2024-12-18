from flask import Flask, request
from flask_socketio import SocketIO
from dotenv import load_dotenv
from pathlib import Path
import os

APP = Flask(__name__)
SOCKET = SocketIO(APP, async_mode='eventlet')

SERVER_DOMAIN = 'https://growvolution.org'

ALL_METHODS = ['GET', 'POST']


@APP.before_request
def log_request():
    from .debugger import log
    method = request.method
    url = request.url
    user_agent = request.headers.get('User-Agent')

    log(f'{method}', f"{url.removeprefix(SERVER_DOMAIN)} [{user_agent}]")


def init_app():

    env_path = Path(__file__).resolve().parent.parent / 'server.env'
    load_dotenv(dotenv_path=env_path)

    APP.config['EXEC_MODE'] = os.getenv('EXEC_MODE')
    APP.config['NRS_PASSWORD'] = os.getenv('NRS_PASSWORD')

    APP.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    APP.config['SERVER_NAME'] = os.getenv('SERVER_NAME')
    APP.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    APP.config['CAPTCHA_KEY'] = os.getenv('SITE_KEY')

    from .views import views
    from .auth import auth

    APP.register_blueprint(views, url_prefix='/')
    APP.register_blueprint(auth, url_prefix='/')

    from .logic import socket

    from .debugger import start_session
    start_session()

    from .mailservice import start
    start()

    from .temporary import start_updater
    start_updater()
