from ...auth.forgot import handle_request
from ..manage import send_message
from ....debugger import log


def handle_event(data):
    log('info', "Forgotten password interface request.")
    send_message('update', handle_request(data))
    log('info', "Update response sent.")
