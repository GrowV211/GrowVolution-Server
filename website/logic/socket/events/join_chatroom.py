from website.data import User
from ..manage import send_message
from ...account.user import user_attributes
from ...conversation.chat import get_chat, render_chat
from ...auth.verify import active_session
from markupsafe import Markup

from ....debugger import log


def handle_event(username):
    session = active_session()

    receiver = User.query.filter_by(username=username).first()
    user = session.user

    chat = get_chat(user, receiver)


    session.set_chat(chat.id)


    chat_html = render_chat(receiver, user_attributes(receiver, False), chat)

    send_message('update', Markup(chat_html))
    log('debug', f"User {user.username} joined chat {chat.id} via {session.sid}.")
