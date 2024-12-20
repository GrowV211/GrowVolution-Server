from flask import request
from . import APP, SOCKET
from .debugger import log

SERVER_DOMAIN = 'https://growvolution.org'
SERVER_IP = 'https://212.132.125.218'


class SocketEvent:
    _events = {}

    def on(self, event):
        def decorator(func):
            self._events[event] = func
            return func
        return decorator

    def handle_event(self, event, data):
        if event in self._events:
            if data:
                self._events[event](data)
            else:
                self._events[event]()
        else:
            log('warn', f"Socket event '{event}' not registered.")


S_EVENTS = SocketEvent()


def socket_event_data(*args):
    event = request.event.get('message', 'unknown')
    data = None

    if event == '*':
        event = args[0]
        data = args[1] if len(args) > 1 else None

    elif len(args) > 1:
        data = args[1]

    return event, data


@APP.before_request
def log_request():
    ip = request.remote_addr
    method = request.method
    url = request.url.removeprefix(SERVER_DOMAIN).removeprefix(SERVER_IP)
    user_agent = request.headers.get('User-Agent')

    log(f'{method}', f"{url} from {ip} with [{user_agent}]")


@SOCKET.on('*')
@SOCKET.on('connect')
@SOCKET.on('disconnect')
@SOCKET.on('message')
def handle_socket_event(*args):
    event, data = socket_event_data(*args)

    log('sock', f"Socket event '{event}' triggered by {request.sid}")

    S_EVENTS.handle_event(event, data)


@APP.errorhandler(Exception)
def handle_exception(e):
    log('error', f"Request of type {request.method}"
                 f" for {request.path} threw {type(e).__name__}: {str(e)}")

    from .basic import render_error
    return render_error()


@SOCKET.on_error_default
def handle_socket_exception(e):
    event, data = socket_event_data(request.event.get('args', None))

    log('error', f"Socket event '{event}'"
                 f" threw {type(e).__name__}: {str(e)}")

    SOCKET.emit('error', f"Socket message '{event}' caused a server-side error.")
