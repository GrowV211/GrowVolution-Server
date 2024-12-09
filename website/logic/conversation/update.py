from flask import request
from website.data import Message, User, add_model
from website.logic.auth.verify import active_user
from .chat import get_chat, get_chat_html


def handle_request():
    data = request.get_json()
    value = data.get('value')

    sender = active_user()
    receiver = User.query.filter_by(username=data.get('receiver')).first()

    if not sender or not receiver:
        return 'Bad Request', 502

    chat = get_chat(sender, receiver)

    if value == 'send':
        content = data.get('content')

        message = Message(sender.id, content, chat.id)
        add_model(message)

    return get_chat_html(chat, receiver)
