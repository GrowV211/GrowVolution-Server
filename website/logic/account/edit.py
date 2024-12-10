from flask import request
from website import APP
from website.basic import render
from werkzeug.utils import secure_filename
from website.data import User
from website.temporary import new_process, lifecycle, TEN_MINUTES, CONFIRM, time_locked, lock
from website.mailservice import send_confirm_mail
from website.logic.auth.verify import active_user
from .user import user_attributes
from pathlib import Path

PROFILE_IMAGE_PATH = Path(APP.static_folder) / 'img' / 'usr'
IMAGE_TEMPLATE = 'basic/account/profile_image.html'


def _confirm(pair):
    user = User.query.filter_by(id=pair[0]).first()
    email = pair[1]
    user.set_email(email)
    return render('auth/email_confirmed.html', email=email)


def _delete_image(user):
    file = (PROFILE_IMAGE_PATH / user.img)
    if file.exists():
        file.unlink()
    user.set_img(None)


def _rename_image(user, new_username):
    if user.img:
        filename = f"{new_username}.jpg"
        (PROFILE_IMAGE_PATH / user.img).rename((PROFILE_IMAGE_PATH / filename))
        user.set_img(filename)


def handle_delete():
    user = active_user()
    _delete_image(user)
    return render(IMAGE_TEMPLATE, user=user_attributes(user, False))

def handle_reset_request():
    user = active_user()
    email = user.email

    temporary = _get_temporary_mail(user.id)
    if temporary:
        email = temporary[0]

    return {
        'user': user.username,
        'email': email,
        'info': user.info
    }


def _get_temporary_mail(user):
    for k, v in CONFIRM.items():
        if isinstance(v[2], tuple) and v[2][0] == user:
            return [v[2][1], k]

    return None


def render_edit(user, attributes):
    email = user.email
    change = 0
    lock_time = 0
    pid = ''

    temporary = _get_temporary_mail(user.id)
    if temporary:
        email = temporary[0]
        pid = temporary[1]
        lock_time = time_locked(pid)
        change = 1

    return render('basic/account/edit.html', username=user.username,
                  user=attributes, first=user.first, last=user.last,
                  email=email, email_change=change, lock=lock_time, pid=pid,
                  info=user.info, changeable=user.username_edit_locked(),
                  lock_days=str(user.username_lock_time()))


def handle_request():
    user = active_user()

    if 'img' in request.files:
        img = request.files['img']

        if user.img:
            _delete_image(user)

        filename = secure_filename(img.filename)
        path = PROFILE_IMAGE_PATH / filename
        img.save(path)

        user.set_img(filename)

        return render(IMAGE_TEMPLATE, user=user_attributes(user, True))


def handle_edit(data):
    user = active_user()

    usr = data.get('user')
    email = data.get('email')
    info = data['info']

    user_hint = False
    email_hint = False
    lock_user = ''
    lock_email = 0
    pid = ''

    if usr and usr != user.username:
        user.set_username(usr)
        _rename_image(user, usr)
        user_hint = True
        lock_user = str(user.username_lock_time())

    if email and email != user.email:
        pid = new_process()
        code = send_confirm_mail(email, user.first)
        lifecycle(CONFIRM, pid, (code, _confirm, (user.id, email)), TEN_MINUTES)
        lock(pid)
        email_hint = True
        lock_email = time_locked(pid)
        pid = pid

    if info != user.info:
        user.set_info(info)

    return {
        'user_hint': user_hint,
        'email_hint': email_hint,
        'lock_user': lock_user,
        'lock_email': lock_email,
        'pid': pid
    }
