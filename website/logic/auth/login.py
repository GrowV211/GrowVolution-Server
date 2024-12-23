from flask import request
from website.basic import render, render_with_flash, goto_login, go_home
from website.data import User
from .verify import captcha_check, active_session, active_user


def handle_request():
    template = 'auth/login.html'
    session = active_session()

    if active_user():
        session.set_user(None)
        return goto_login()

    if request.method == "POST":

        check = captcha_check()

        if check:
            return render_with_flash(template, check, 'danger')

        acc = request.form['user']
        user = User.query.filter((User.username == acc) | (User.email == acc)).first()

        if user and user.check_psw(request.form['psw']):
            session.set_user(user.id)
            session.csrf(False)
            return go_home()
        elif user:
            return render_with_flash(template, "Falsches Passwort!", 'danger',
                                     user=acc, csrf_token=session.csrf())
        else:
            return render_with_flash(template, "Benutzer nicht gefunden! Falls du noch kein Konto hast, "
                                               "kannst du <a href='/signup'>hier</a> eins eröffnen.", 'warning',
                                     csrf_token=session.csrf())

    return render(template, csrf_token=session.csrf())
