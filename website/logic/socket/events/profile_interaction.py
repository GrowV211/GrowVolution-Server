from flask import request
from ....data import User
from ..manage import send_message, get_socket
from ...auth.verify import active_user
from ...account.user import handle_interaction


def handle_event(data):
    sid = request.sid
    socket = get_socket(sid)
    user = User.query.filter_by(username=socket.tab).first()

    send_message('update', handle_interaction(user, user == active_user(), data))
