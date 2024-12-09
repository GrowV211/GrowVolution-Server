from website.basic import render, render_404
from website.temporary import CONFIRM, RESET, first_locked, time_locked, lock
from website.data import User


def _check_lock(pid):
    if not first_locked(pid):
        lock(pid)


def handle_request(pid):
    if pid in CONFIRM:
        data = CONFIRM[pid]

        model = data[2]

        _check_lock(pid)

        return render('auth/notice.html', user=model.first,
                      email=model.email, time=time_locked(pid))

    elif pid in RESET:
        user = User.query.filter_by(id=RESET[pid][1]).first()

        _check_lock(pid)

        return render('auth/reset_notice.html', user=user.first,
                      email=user.email, time=time_locked(pid))

    return render_404()
