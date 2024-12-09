from flask import request
from website.data import User
from website import APP
import jwt


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
