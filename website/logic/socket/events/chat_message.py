from flask import request
from ...conversation.update import handle_request
from ..manage import send_message


def handle_event(data):
    response = handle_request(data, request.sid)
    print(response)
    send_message('update_chat', response)
