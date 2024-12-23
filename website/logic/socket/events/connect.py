from flask import request
from flask_socketio import disconnect, emit
from website import APP
from ...auth.verify import active_user, active_session


def handle_event():
    user = active_user()
    session = active_session()

    if session.sid:
        disconnect(session.sid)

    active_session().set_socket(request.sid)

    emit('connect_info', {
        'exec': APP.config['EXEC_MODE'],
        'has_user': bool(user)
    })
