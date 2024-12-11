from flask import request
from ...conversation.update import handle_request
from ..manage import send_message
from ....debugger import log


def handle_event(data):
    sid = request.sid
    log('info', f"Chat message received via '{sid}'.")
    send_message('update_chat', handle_request(data, sid))
    log('info', "Chat updated.")
