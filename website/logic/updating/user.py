from website.debugger import log
from website.data import User


def update(date):
    for user in User.query.all():
        user.update_username_lock()

        if not user.has_done_journal(date):
            user.update_score(-10)

    log('info', "All users updated.")