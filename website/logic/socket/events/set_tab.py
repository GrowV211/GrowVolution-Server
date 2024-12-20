from flask import request
from ..manage import get_socket


def handle_event(tab):
    sid = request.sid
    socket = get_socket(sid)
    socket.set_active_tab(tab)
