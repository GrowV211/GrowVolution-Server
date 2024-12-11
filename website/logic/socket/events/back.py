from flask import request
from ....basic import render
from ....data import User
from ..manage import get_socket, send_message, leave_chatroom
from ...auth.verify import active_user
from ...conversation import chats
from ...account.user import render_profile
from markupsafe import Markup
from ....debugger import log


def handle_event():
    sid = request.sid
    socket = get_socket(sid)
    socket_tab = socket.tab

    log('info', f"Back navigation via '{sid}' at '{socket_tab}'.")

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

    log('info', "Update response sent.")
