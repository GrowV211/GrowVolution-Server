from flask import request
from website.basic import render, render_404
from website.temporary import RESET, clear
from website.data import User


def _handle_fetch(user):
    psw = request.get_json().get('value')
    user.set_psw_crypt(psw)

    return render('auth/reset_success.html')


def handle_request(code):
    for k, v in RESET.items():
        if v[0] == code:
            user = User.query.filter_by(id=v[1]).first()

            if request.is_json:
                clear(k)
                return _handle_fetch(user)

            return render('auth/reset.html', email=user.email)

    return render_404()
