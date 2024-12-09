from flask import make_response, redirect


def clear_token(destination):
    response = make_response(redirect(f'/{destination}'))
    response.set_cookie('token', '', expires=0)
    return response


def handle_request():
    return clear_token('')
