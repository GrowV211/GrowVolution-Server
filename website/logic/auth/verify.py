from flask import request
from website.data import Session
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

    if not result.get("success") or result.get("score", 0) < 0.66:
        log('warn', "Failed captcha check!")
        return "Du wurdest von reCAPTCHA als unvertrauenswürdig eingestuft!"

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
    return active_session().user if session.userID else None


def session_data():
    decoded = _decoded_token(request.cookies.get('token'))
    return decoded


def active_session():
    data = session_data()
    return Session.query.filter_by(id=data['session_id']).first()
