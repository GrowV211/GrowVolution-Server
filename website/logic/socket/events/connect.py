from flask import request
from flask_socketio import disconnect, emit
from website import APP
from ...auth.verify import active_session


def handle_event():
    session = active_session()

    if not session:
        emit('reload')
        return

    if session.sid:
        disconnect(session.sid)

    session.set_socket(request.sid)

    emit('connect_info', {
        'exec': APP.config['EXEC_MODE']
    })
