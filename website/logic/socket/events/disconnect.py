from flask import request
from ..manage import get_socket
from website.data import delete_model


def handle_event():
    socket = get_socket(request.sid)
    delete_model(socket)