from flask import request
from website.data import User
from website import APP
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
        return "Du wurdest von reCAPTCHA als Bot eingestuft!"

    return None


def _active_user(token):
    if token:
        try:
            decoded = jwt.decode(token, key=APP.config['SECRET_KEY'], algorithms=['HS256'])
            user = User.query.filter_by(id=decoded['user_id']).first()
            return user
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except jwt.InvalidSignatureError:
            return None

    return None


def active_user():
    user = _active_user(request.cookies.get('token'))
    if user:
        return user

    return None


def is_remembered():
    if active_user():
        return True

    return False
