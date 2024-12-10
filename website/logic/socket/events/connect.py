from flask import request
from flask_socketio import disconnect
from website.data import Socket, add_model, delete_model
from ..manage import update_chatroom
from ...auth.verify import active_user
from datetime import datetime


def handle_event():
    user = active_user()

    if not user:
        socket = Socket(request.sid)
        add_model(socket)
        print(
            f"127.0.0.1 - - [{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] New Socket established without active user.")

    else:
        existing = Socket.query.filter_by(userID=user.id).first()

        if existing:
            update_chatroom(existing.id, request.sid)
            disconnect(existing.id)
            delete_model(existing)
            print(
                f"127.0.0.1 - - [{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Closed connection to existing socket.")

        socket = Socket(request.sid, user.id)
        add_model(socket)
        print(
            f"127.0.0.1 - - [{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] New Socket established with active user.")
