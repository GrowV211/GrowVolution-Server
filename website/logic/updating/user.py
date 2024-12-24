from website.debugger import log
from website.data import User, Password
from website.crypt import decrypt_bytes


def update(date):
    for user in User.query.all():
        user.update_username_lock()

        if not user.has_done_journal(date):
            user.update_score(-10)

    log('info', "All users updated.")


def update_passwords(old_psw, mode):
    for password in Password.query.filter_by(storage_mode=mode).all():
        password.safe_password(decrypt_bytes(password.enc_psw, old_psw))

    log('info', f"{mode} passwords updated.")
