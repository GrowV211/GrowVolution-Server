from flask import request
from website.data import User, Session
from website import APP
from website.debugger import log
import requests
import jwt
import os

API_KEY = os.getenv('API_KEY')


def captcha_check():
    recaptcha_response = request.form.get('g-recaptcha-response')

    if not recaptcha_response:
        return "Es wurde keine reCAPTCHA übergeben!"

    verification_url = "https://www.google.com/recaptcha/api/siteverify"
    data = {
        'secret': API_KEY,
        'response': recaptcha_response
    }
    response = requests.post(verification_url, data=data)
    result = response.json()

    if not result.get("success") or result.get("score", 0) < 0.5:
        log('warn', "Failed captcha check!")
        return "Du wurdest von reCAPTCHA als Bot eingestuft!"

    return None


def _decoded_token(token):
    try:
        return jwt.decode(token, key=APP.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except jwt.InvalidSignatureError:
        return None


def active_user():
    session = active_session()
    return active_session().user if session else None


def is_remembered():
    if active_user():
        return True

    return False


def active_session_id():
    decoded = _decoded_token(request.cookies.get('token'))
    return decoded['session_id'] if decoded else None


def active_session():
    session_id = active_session_id()
    return Session.query.filter_by(id=session_id).first() if session_id else None
