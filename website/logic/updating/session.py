from website import SOCKET
from website.data import Session, delete_model
from sqlalchemy.sql import func
from website.debugger import log
from ..socket.manage import send_message


def clear_expired(now):
    expired = Session.query.filter(func.datetime(Session.timestamp, '+1 hour') < now).all()
    for session in expired:
        sid = session.sid
        user = session.user if session.userID else None

        if sid:
            send_message('reload', None, sid)
            SOCKET.disconnect(sid)

        delete_model(session)

        if user:
            check_user_sessions(user)

    log('info', "Expired sessions cleared.")


def check_user_sessions(user):
    if not user.sessions:
        user.password.update_storage_mode('RECOVER')
