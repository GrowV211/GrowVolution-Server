from flask import request, make_response, redirect
from website.temporary import _calc_seconds
from website.basic import render, render_with_flash
from website.data import User
from website import APP
from .verify import is_remembered
from .logout import clear_token
import datetime
import jwt


def token_response(uid, remember):
    token = jwt.encode({
        'user_id': uid,
        'exp': datetime.datetime.now() + datetime.timedelta(days=30 if remember else 1)
    }, APP.config['SECRET_KEY'], algorithm='HS256')

    response = make_response(redirect('/'))
    response.set_cookie('token', token, httponly=True,
                        max_age=_calc_seconds("30:00:00:00") if remember else _calc_seconds("01:00:00:00"))

    return response


def handle_request():
    template = 'auth/login.html'

    if is_remembered():
        return clear_token('login')

    if request.method == "POST":
        acc = request.form['user']
        user = User.query.filter((User.username == acc) | (User.email == acc)).first()
        remember = 'remember' in request.form

        if user and user.check_psw(request.form['psw']):
            return token_response(user.id, remember)
        elif user:
            return render_with_flash(template, "Falsches Passwort!", 'danger', user=acc)
        else:
            return render_with_flash(template, "Benutzer nicht gefunden! Falls du noch kein Konto hast, "
                                               "kannst du <a href='/signup'>hier</a> eins eröffnen.", 'warning')

    return render(template)
