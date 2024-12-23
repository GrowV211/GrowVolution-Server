from flask import Flask
from flask_socketio import SocketIO
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from pathlib import Path
import os

APP = Flask(__name__)
SOCKET = SocketIO(APP, async_mode='eventlet')
APP.wsgi_app = ProxyFix(APP.wsgi_app, x_for=1, x_proto=1)
LIMITER = Limiter(get_remote_address, app=APP, default_limits=["500 per day", "100 per hour"])

ALL_METHODS = ['GET', 'POST']


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
