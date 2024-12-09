from . import SOCKET
from flask import request
from flask_socketio import emit, disconnect
from .basic import render
from .logic.auth.verify import active_user
from .logic.auth import forgot
from .logic.account import available
from .logic.conversation import chat, chats, update
from .data import Socket, add_model, delete_model, Chatroom
from markupsafe import Markup
from datetime import datetime


@SOCKET.on('connect')
def on_connect():
    user = active_user()

    if not user:
        print(f"127.0.0.1 - - [{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] New Socket established without active user.")

    else:
        existing = Socket.query.filter_by(userID=user.id).first()

        if existing:
            _update_chatroom(existing.id, request.sid)
            disconnect(existing.id)
            delete_model(existing)
            print(f"127.0.0.1 - - [{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Closed connection to existing socket.")

        socket = Socket(request.sid, user.id)
        add_model(socket)
        print(f"127.0.0.1 - - [{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] New Socket established with active user.")


def get_socket(user):
    socket = Socket.query.filter_by(userID=user).first()
    return socket if socket else None


def send_update(socket, key, value):
    emit(key, value, to=socket)


@SOCKET.on('set_tab')
def set_tab(tab):
    socket = Socket.query.filter_by(id=request.sid).first()
    if socket:
        socket.set_active_tab(tab)


@SOCKET.on('disconnect')
def on_disconnect():
    socket = Socket.query.filter_by(id=request.sid).first()

    if socket:
        delete_model(socket)


@SOCKET.on('back')
def back(destination):
    if destination == 'login':
        emit('update', {
            'value': 'html',
            'html': Markup(render('auth/login_form.html')),
            'type': 'login'
        })

    elif destination == 'chats':
        _close_chatroom()
        emit('update', {
            'html': Markup(chats.get_chat_list(active_user())),
            'type': 'chats'
        })


@SOCKET.on('forgot_query')
def on_forgot_query(data):
    emit('update', forgot.handle_request(data))


@SOCKET.on('availability_check')
def availability_check(data):
    emit('availability_response', available.handle_request(data))


@SOCKET.on('open_chatroom')
def open_chatroom(data):
    emit('update', {
        'html': Markup(chat.handle_request(data, request.sid)),
        'type': 'chat'
    })


def _update_chatroom(previous_sid, new_sid):
    chatroom = Chatroom.query.filter_by(socketID=previous_sid).first()
    if chatroom:
        chatroom.update_socket(new_sid)


def _close_chatroom():
    chatroom = Chatroom.query.filter_by(socketID=request.sid).first()
    if chatroom:
        delete_model(chatroom)


@SOCKET.on('chat_message')
def chat_message(data):
    emit('update_chat', update.handle_request(data, request.sid))
