from flask import request
from ..manage import get_socket
from ....debugger import log


def handle_event(tab):
    sid = request.sid
    log('info', f"Setting tab for '{sid}' to '{tab}'.")
    socket = get_socket(sid)
    socket.set_active_tab(tab)
    log('info', "New socket tab set.")
