from flask import request
from flask_socketio import emit
from website.data import Socket, Chatroom, add_model, delete_model



def get_socket(socket_id=None, user_id=None):
    if socket_id:
        socket = Socket.query.filter_by(id=socket_id).first()

    else:
        socket = Socket.query.filter_by(userID=user_id).first()

    return socket


def send_message(key, value, socket_id=None):
    if socket_id:
        emit(key, value, to=socket_id)

    else:
        emit(key, value)


def join_chatroom(chat):
    chatroom = Chatroom(request.sid, chat)
    add_model(chatroom)


def update_chatroom(previous_sid, new_sid):
    chatroom = Chatroom.query.filter_by(socketID=previous_sid).first()
    if chatroom:
        chatroom.update_socket(new_sid)


def leave_chatroom():
    chatroom = Chatroom.query.filter_by(socketID=request.sid).first()
    if chatroom:
        delete_model(chatroom)