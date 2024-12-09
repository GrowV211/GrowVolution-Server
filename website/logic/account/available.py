from flask import request, jsonify
from website.data import User
from website.logic.auth.verify import active_user


def handle_request(data):
    available = False

    if data['type'] == 'username':
        if User.query.filter_by(username=data['value']).first():
            available = True
    else:
        user = User.query.filter_by(email=data['value']).first()
        if user and user != active_user():
            available = True

    return {
        'type': data['type'],
        'available': available
    }
