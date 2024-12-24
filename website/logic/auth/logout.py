from flask import redirect
from .verify import active_session
from ..updating.session import check_user_sessions


def handle_request():
    session = active_session()
    uid = session.userID

    if uid:
        user = session.user
        session.set_user(None)
        check_user_sessions(user)

    return redirect('/')
