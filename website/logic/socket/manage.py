from ... import SOCKET
from flask import request


def send_message(key, value, socket_id=None):
    if socket_id:
        SOCKET.emit(key, value, to=socket_id)

    else:
        SOCKET.emit(key, value, to=request.sid)