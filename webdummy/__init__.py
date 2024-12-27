from flask import Flask, render_template, redirect
from pathlib import Path
from dotenv import load_dotenv
import os
APP = Flask(__name__)


@APP.route('/')
def maintenance():
    return render_template('offline.html')


@APP.route('/about')
def about():
    return render_template('about.html')


@APP.route('/privacy')
def privacy():
    return render_template('privacy.html')


@APP.route('/impressum')
def impressum():
    return render_template('impressum.html')


@APP.route('/<path:path>')
def go_home(path):
    return redirect('/')


def init_app():
    env_path = Path(__file__).resolve().parent.parent / 'server.env'
    load_dotenv(dotenv_path=env_path)

    APP.config['SERVER_NAME'] = os.getenv('SERVER_NAME')
    APP.config['SECRET_KEY'] = os.getenv('DUMMY_KEY')
