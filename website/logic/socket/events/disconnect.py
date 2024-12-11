from flask import request
from ..manage import get_socket
from website.data import delete_model
from ....debugger import log


def handle_event():
    sid = request.sid
    socket = get_socket()
    delete_model(socket)
    log('info', f"Socket connection via '{sid}' now disconnected.")