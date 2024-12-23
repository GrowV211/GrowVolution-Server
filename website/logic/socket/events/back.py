from ....basic import render
from ....data import User
from ..manage import send_message
from ...auth.verify import active_user, active_session
from ...conversation import chats
from ...account.user import render_profile
from markupsafe import Markup


def handle_event():
    session = active_session()
    session_tab = session.tab

    if session_tab == 'home':
        pass

    elif session_tab == 'login':
        send_message('update', {
            'value': 'html',
            'html': Markup(render('auth/login_form.html')),
            'type': 'login'
        })

    elif session_tab == 'chats':
        session.set_chat(None)
        send_message('update', {
            'html': Markup(chats.get_chat_list(active_user())),
            'type': 'chats'
        })

    else:
        user = User.query.filter_by(username=session_tab).first()

        if user:
            session.set_chat(None)
            send_message('update', Markup(render_profile(user, True, user == active_user())))
