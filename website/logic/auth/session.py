from flask import make_response, redirect, request, session, flash
from ... import APP
from ...temporary import _calc_seconds, ONE_HOUR
from ...data import Session, add_model
from .verify import session_data
from uuid import uuid4
import datetime
import jwt

BOT_AGENTS = [
    "zgrab",
    "curl",
    "wget",
    "python-requests",
    "java",
    "libwww-perl",
    ".net clr",
    "headlesschrome",
    "phantomjs",
    "selenium"
]


def clear_token(path):
    return token_response({
        'session_id': session_data(),
        'session_ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent')
    }, path)


def token_response(data, path):
    data['exp'] = datetime.datetime.now() + datetime.timedelta(hours=1)
    token = jwt.encode(data, APP.config['SECRET_KEY'], algorithm='HS256')

    response = make_response(redirect(path))
    response.set_cookie('token', token, httponly=True,
                        max_age=_calc_seconds(ONE_HOUR))

    return response


def _refuse_request(msg):
    from ...debugger import log
    log('warn', msg)
    return f"500 - {msg}", 500


def _verify_new_session(user_agent):
    str_user_agent = str(user_agent).lower()

    if request.method == "POST":
        return _refuse_request("Unauthorized request!")

    elif not user_agent:
        return _refuse_request("No user agent!")

    for agent in BOT_AGENTS:
        if agent in str_user_agent:
            return _refuse_request("Unauthorized user agent!")

    return None


def _verify_active_session(data, sess):
    from ...debugger import log

    if data and data['session_ip'] != request.remote_addr or data['user_agent'] != request.headers.get('User-Agent'):
        log('warn', "Mismatching requestor identification attributes!")
        sess.set_invalid()
        return _refuse_request("Requestor identification failed!")

    elif request.method == "POST":
        if not request.form.get('csrf') == sess.csrf_token:
            log('warn', "CSRF token mismatch!")

            if not session.get('invalid_csrf'):
                session['invalid_csrf'] = 1
            else:
                session['invalid_csrf'] += 1

            flash("Dein CSRF Token ist ungültig!", "danger")
            return redirect(request.path)

    elif session.get('invalid_csrf') and session['invalid_csrf'] > 3:
        log('warn', "Too many invalid CSRF checks - session blocked!")
        sess.set_invalid()
        session.clear()
        return _refuse_request("Session blocked due to too many invalid CSRF checks!")

    return None


def _track_activity(path):
    if 'static' in path:
        if session.get('static_requests'):
            session['static_requests'] += 1
        else:
            session['static_requests'] = 1

    else:
        if session.get('dynamic_requests'):
            session['dynamic_requests'] += 1
        else:
            session['dynamic_requests'] = 1


def _check_activity(sess):
    from ...debugger import log
    dynamic = session.get('dynamic_requests')
    static = session.get('static_requests')

    if dynamic and dynamic > 5 and not static:
        log('warn',
            f"Suspicious activity - missing static requests from {request.remote_addr}!")
        sess.set_invalid()
        session.clear()
        return _refuse_request("Session blocked due to suspicious activity!")

    elif dynamic and dynamic > 5 and not sess.verified:
        log('warn', "Suspicious activity - unverified session!")
        sess.set_invalid()
        session.clear()
        return _refuse_request("Session has not been verified and will be blocked!")

    return None


def handle_session(path):
    data = session_data()
    sess = Session.query.filter_by(id=data['session_id']).first() if data else None

    if sess and not sess.valid:
        return _refuse_request("Session invalid!")

    if not data or not sess:
        session.clear()
        user_agent = request.headers.get('User-Agent')

        new_session_invalid = _verify_new_session(user_agent)
        if new_session_invalid:
            return new_session_invalid

        sess = Session(uuid4())
        add_model(sess)

        return token_response({
            'session_id': sess.id,
            'session_ip': request.remote_addr,
            'user_agent': user_agent
        }, path)

    session_invalid = _verify_active_session(data, sess)
    if session_invalid:
        return session_invalid

    _track_activity(path)

    activity_check = _check_activity(sess)
    if activity_check:
        return activity_check

    return None
