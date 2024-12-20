from flask import request
from flask_socketio import disconnect, emit
from website import APP
from website.data import Socket, add_model, delete_model
from ..manage import update_chatroom
from ...auth.verify import active_user


def handle_event():
    user = active_user()

    if not user:
        sid = request.sid
        socket = Socket(sid)
        add_model(socket)

    else:
        existing = Socket.query.filter_by(userID=user.id).first()
        sid = request.sid

        if existing:
            e_sid = existing.id
            update_chatroom(e_sid, sid)
            disconnect(e_sid)
            delete_model(existing)

        socket = Socket(sid, user.id)
        add_model(socket)

    emit('connect_info', {
        'exec': APP.config['EXEC_MODE'],
        'has_user': bool(user)
    })
