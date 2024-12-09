from flask import jsonify
from website.temporary import CONFIRM, RESET, lock, time_locked
from website.messaging import send_confirm_mail, send_reset_link
from website.data import User


def handle_request(pid):
    if pid in CONFIRM:
        data = CONFIRM[pid]
        element = data[2]

        if isinstance(element, tuple):
            user = User.query.filter_by(id=element[0]).first()
            code = send_confirm_mail(element[1], user.first)
        else:
            code = send_confirm_mail(element.email, element.first)

        CONFIRM[pid] = (code, data[1], element)

        lock(pid)

        return jsonify(lock_time=time_locked(pid))

    elif pid in RESET:
        data = RESET[pid]
        user = User.query.filter_by(id=data[1]).first()
        code = send_reset_link(user.email, user.first)

        RESET[pid] = (code, data[1])

        lock(pid)

        return jsonify(lock_time=time_locked(pid))
