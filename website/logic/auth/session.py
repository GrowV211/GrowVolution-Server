from flask import make_response, redirect, request
from ... import APP
from ...temporary import _calc_seconds, ONE_HOUR, session_lifecycle
from ...data import Session, add_model
from .verify import active_session_id
from uuid import uuid4
import datetime
import jwt


def clear_token(path):
    return token_response({
        'session_id': active_session_id()
    }, path)


def token_response(data, path):
    data['exp'] = datetime.datetime.now() + datetime.timedelta(hours=1)
    token = jwt.encode(data, APP.config['SECRET_KEY'], algorithm='HS256')

    response = make_response(redirect(path))
    response.set_cookie('token', token, httponly=True,
                        max_age=_calc_seconds(ONE_HOUR))

    return response


def handle_session(path):
    session_id = active_session_id()
    if not session_id:
        if request.method == "POST":
            from ...debugger import log
            log( 'warn',"Unauthorized request!")
            return "500 Unauthorized Request!", 500

        session = Session(uuid4())
        add_model(session)
        session_lifecycle(session.id)
        return token_response({
            'session_id': session.id
        }, path)

    return None
