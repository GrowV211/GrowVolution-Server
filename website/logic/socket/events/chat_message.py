from flask import request
from ...conversation.update import handle_request
from ..manage import send_message


def handle_event(data):
    sid = request.sid
    send_message('update_chat', handle_request(data, sid))
