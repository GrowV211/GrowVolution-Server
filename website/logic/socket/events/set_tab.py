from flask import request
from ..manage import get_socket


def handle_event(tab):
    socket = get_socket(request.sid)
    socket.set_active_tab(tab)