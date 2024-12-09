from flask import render_template, request
from website.basic import render, goto_login
from website.data import User
from ..account.user import user_attributes
from ..auth.verify import active_user
from .chat import render_chat, get_chat
from markupsafe import Markup


def _render_chat(user, participant, chat):
    return render_template('basic/conversation/chat_list_element.html', type='profile-picture',
                           user=user_attributes(participant, False), username=participant.username,
                           unread_messages=user.get_unread_chat_messages(chat),
                           message=chat.get_last_message_text(user))


def _get_chat_list(user):
    chats = ''

    for chat in user.chats:
        for participant in chat.participants:
            if participant != user:
                chats += _render_chat(user, participant, chat)
                break

    return Markup(chats)


def _handle_fetch():
    data = request.get_json()
    value = data.get('value')
    user = active_user()

    if value == "chat":
        receiver = User.query.filter_by(username=data.get('receiver')).first()
        return render_chat(receiver, user_attributes(receiver, False), get_chat(user, receiver))

    return _get_chat_list(user)


def handle_request():
    user = active_user()

    if not user:
        return goto_login()

    if request.is_json:
        return _handle_fetch()

    return render('basic/conversation/chats.html', chats=_get_chat_list(user))
