from flask import render_template
from website.basic import render, goto_login
from ..account.user import user_attributes
from ..auth.verify import active_user
from markupsafe import Markup


def _render_chat(user, participant, chat):
    return render_template('basic/conversation/chat_list_element.html', type='profile-picture',
                           user=user_attributes(participant, False), username=participant.username,
                           unread_messages=user.get_unread_chat_messages(chat),
                           message=chat.get_last_message_text(user))


def get_chat_list(user):
    chats = ''

    for chat in user.chats:
        for participant in chat.participants:
            if participant != user:
                chats += _render_chat(user, participant, chat)
                break

    return Markup(chats)


def handle_request():
    user = active_user()

    if not user:
        return goto_login()

    return render('basic/conversation/chats.html', chats=get_chat_list(user))
