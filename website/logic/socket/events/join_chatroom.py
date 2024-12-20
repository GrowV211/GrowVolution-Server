from website.data import User
from ..manage import join_chatroom, send_message
from ...account.user import user_attributes
from ...conversation.chat import get_chat, render_chat
from ...auth.verify import active_user
from markupsafe import Markup


def handle_event(username):

    receiver = User.query.filter_by(username=username).first()
    user = active_user()

    chat = get_chat(user, receiver)

    join_chatroom(chat)

    chat_html = render_chat(receiver, user_attributes(receiver, False), chat)

    send_message('update', Markup(chat_html))
