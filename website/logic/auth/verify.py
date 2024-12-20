from flask import request
from website.data import User
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
    token = request.cookies.get('token')
    if token:
        decoded = _decoded_token(token)
        if decoded:
            user = User.query.filter_by(id=decoded['user_id']).first()
            if user:
                return user

    return None


def is_remembered():
    if active_user():
        return True

    return False
