from flask import redirect
from .verify import active_session

def handle_request():
    session = active_session()

    if session.userID:
        session.set_user(None)

    return redirect('/')
