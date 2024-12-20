from flask import request
from ..manage import get_socket
from website.data import delete_model


def handle_event():
    sid = request.sid
    socket = get_socket(sid)
    delete_model(socket)