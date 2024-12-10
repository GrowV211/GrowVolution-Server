from website import SOCKET
from .events import (connect, disconnect, back, set_tab,
                     join_chatroom, availability_check, forgot_query,
                     chat_message, resend_mail, profile_interaction)
from ..account.edit import handle_edit, handle_reset_request, handle_delete
from .manage import send_message


@SOCKET.on('connect')
def on_connect():
    connect.handle_event()


@SOCKET.on('disconnect')
def on_disconnect():
    disconnect.handle_event()


@SOCKET.on('back')
def on_back():
    back.handle_event()


@SOCKET.on('set_tab')
def on_set_tab(tab):
    set_tab.handle_event(tab)


@SOCKET.on('availability_check')
def on_availability_check(data):
    availability_check.handle_event(data)


@SOCKET.on('forgot_query')
def on_forgot_query(data):
    forgot_query.handle_event(data)


@SOCKET.on('resend_mail')
def on_resend(pid):
    resend_mail.handle_event(pid)


@SOCKET.on('profile_interaction')
def on_profile_interaction(data):
    profile_interaction.handle_event(data)


@SOCKET.on('edit_profile')
def on_edit_profile(data):
    send_message('profile_update', handle_edit(data))


@SOCKET.on('reset_edit')
def on_reset_edit():
    send_message('edit_reset', handle_reset_request())


@SOCKET.on('delete_pp')
def on_pp_delete():
    send_message('pp_delete', handle_delete())


@SOCKET.on('join_chatroom')
def on_join_chatroom(username):
    join_chatroom.handle_event(username)


@SOCKET.on('chat_message')
def on_chat_message(data):
    chat_message.handle_event(data)
