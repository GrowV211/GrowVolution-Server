from flask import request
from website.data import User
from ..manage import join_chatroom, send_message, get_socket
from ...account.user import user_attributes
from ...conversation.chat import get_chat, render_chat
from ...auth.verify import active_user
from markupsafe import Markup


def handle_event(username):
    receiver = User.query.filter_by(username=username).first()
    user = active_user()

    chat = get_chat(user, receiver)

    join_chatroom(chat.id)

    chat_html = render_chat(receiver, user_attributes(receiver, False), chat)

    print(username)

    send_message('update', Markup(chat_html))
