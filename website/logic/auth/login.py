from flask import request
from website.basic import render, render_with_flash
from website.data import User
from .verify import is_remembered, captcha_check, active_session_id
from .session import token_response, clear_token
from ..socket.manage import send_message


def handle_request():
    template = 'auth/login.html'

    if is_remembered():
        return clear_token('/login')

    if request.method == "POST":

        check = captcha_check()

        if check:
            return render_with_flash(template, check, 'danger')

        acc = request.form['user']
        user = User.query.filter((User.username == acc) | (User.email == acc)).first()

        if user and user.check_psw(request.form['psw']):
            return token_response({
                'user_id': user.id,
                'session_id': active_session_id()
            }, '/')
        elif user:
            return render_with_flash(template, "Falsches Passwort!", 'danger', user=acc)
        else:
            return render_with_flash(template, "Benutzer nicht gefunden! Falls du noch kein Konto hast, "
                                               "kannst du <a href='/signup'>hier</a> eins eröffnen.", 'warning')

    return render(template)
