from flask import request
from website.basic import render, render_with_flash, goto_login, go_home
from website.data import User, Password, add_model
from .verify import captcha_check, active_session, active_user


def handle_request():
    template = 'auth/login.html'
    session = active_session()

    if active_user():
        session.set_user(None)
        session.unset_password()
        return goto_login()

    if request.method == "POST":

        check = captcha_check()

        if check:
            return render_with_flash(template, check, 'danger')

        acc = request.form['user']
        user = User.query.filter((User.username == acc) | (User.email == acc)).first()

        psw = request.form['psw']

        if user and psw and user.check_psw(psw):
            session.set_user(user.id)
            session.csrf(False)

            if not user.password:
                password = Password(user.id)
                add_model(password)
                password.safe_password(psw)

            return go_home()

        elif user:
            return render_with_flash(template, "Falsches Passwort!", 'danger',
                                     user=acc, csrf_token=session.csrf())
        else:
            return render_with_flash(template, "Benutzer nicht gefunden! Falls du noch kein Konto hast, "
                                               "kannst du <a href='/signup'>hier</a> eins eröffnen.", 'warning',
                                     csrf_token=session.csrf())

    return render(template, csrf_token=session.csrf())
