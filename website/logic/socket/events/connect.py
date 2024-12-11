from flask import request
from flask_socketio import disconnect, emit
from website import EXEC_MODE
from website.debugger import log
from website.data import Socket, add_model, delete_model
from ..manage import update_chatroom
from ...auth.verify import active_user


def handle_event():
    user = active_user()

    if not user:
        socket = Socket(request.sid)
        add_model(socket)
        log('info', "New socket connection without active user.")

    else:
        existing = Socket.query.filter_by(userID=user.id).first()

        if existing:
            update_chatroom(existing.id, request.sid)
            disconnect(existing.id)
            delete_model(existing)
            log('info', "Existing connection updated on reconnect.")

        socket = Socket(request.sid, user.id)
        add_model(socket)
        log('info', "New socket connection with active user.")

    emit('connect', EXEC_MODE)
