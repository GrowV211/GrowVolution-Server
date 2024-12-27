from website import SOCKET
from website.data import Session, delete_model
from sqlalchemy.sql import func, text
from website.debugger import log
from ..socket.manage import send_message


def clear_expired(now):
    expired = Session.query.filter(func.date_add(Session.timestamp,
                                                 text("INTERVAL 1 HOUR")) < now).all()

    for session in expired:
        sid = session.sid

        if sid:
            send_message('reload', None, sid)
            SOCKET.disconnect(sid)

        delete_model(session)

    log('info', "Expired sessions cleared.")
