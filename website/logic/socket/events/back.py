from flask import request
from website.basic import render
from website.data import User
from ..manage import get_socket, send_message, leave_chatroom
from ...auth.verify import active_user
from ...conversation import chats
from ...account.user import render_profile
from markupsafe import Markup


def handle_event():
    socket = get_socket(request.sid)
    socket_tab = socket.tab

    if socket_tab == 'home':
        pass

    elif socket_tab == 'login':
        send_message('update', {
            'value': 'html',
            'html': Markup(render('auth/login_form.html')),
            'type': 'login'
        })

    elif socket_tab == 'chats':
        leave_chatroom()
        send_message('update', {
            'html': Markup(chats.get_chat_list(active_user())),
            'type': 'chats'
        })

    else:
        user = User.query.filter_by(username=socket_tab).first()

        if user:
            leave_chatroom()
            send_message('update', Markup(render_profile(user, True, user == active_user())))
