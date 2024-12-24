import time
import threading
import random
from . import APP, SOCKET
from .debugger import log
from .logic.updating import user, session
from .logic.socket.manage import send_message
from datetime import datetime, timedelta
import secrets
import string

ONE_DAY = "01:00:00:00"
ONE_HOUR = "00:01:00:00"
TEN_MINUTES = "00:00:10:00"

CONFIRM = {}
LOCK = {}
TIMES_LOCKED = {}

RESET = {}

TMP_PASSWORD = ""
RECOVERY_PSW = ""
CHARSET = string.ascii_letters + string.digits + string.punctuation


def _update_password_tmp():
    global TMP_PASSWORD
    TMP_PASSWORD = ''.join(secrets.choice(CHARSET) for _ in range(16))


def _update_password_recovery():
    global RECOVERY_PSW
    RECOVERY_PSW = ''.join(secrets.choice(CHARSET) for _ in range(32))


def _calc_seconds(time_string):
    d, h, m, s = map(int, time_string.split(":"))
    return s + m * 60 + h * 3600 + d * 24 * 3600


def _cycle(base, key, seconds):
    while seconds > 0:
        if key not in base:
            return

        seconds -= 1
        time.sleep(1)

    clear(key)


def new_process():
    return str(random.randint(100000, 999999))


def lifecycle(base, key, value, lifetime):
    base[key] = value

    threading.Thread(target=_cycle, args=(base, key, _calc_seconds(lifetime))).start()


def _lockcycle(key):
    seconds = LOCK[key]
    while seconds > 0:
        if key not in LOCK:
            return

        LOCK[key] -= 1
        time.sleep(1)

    LOCK.pop(key)


def lock(key):
    if first_locked(key):
        TIMES_LOCKED[key] += 1
    else:
        TIMES_LOCKED[key] = 1

    LOCK[key] = 60 * TIMES_LOCKED[key]

    threading.Thread(target=_lockcycle, args=(key,)).start()


def first_locked(key):
    if key in TIMES_LOCKED:
        return True

    return False


def time_locked(key):
    if key in LOCK:
        return LOCK[key]

    return 0


def clear(key):
    if key in CONFIRM:
        CONFIRM.pop(key)
    if key in RESET:
        RESET.pop(key)
    if key in LOCK:
        LOCK.pop(key)
    if key in TIMES_LOCKED:
        TIMES_LOCKED.pop(key)


def _remaining_seconds():
    now = datetime.now()
    end_of_day = datetime.combine(now.date(), datetime.max.time())
    remaining = end_of_day - now

    return int(remaining.total_seconds())


def _update_users(date):
    log('info', "Updating user database...")
    with APP.app_context():
        user.update(date)


def _clear_sessions():
    log('info', "Clearing expired sessions...")
    with APP.app_context():
        session.clear_expired(datetime.now())


def _update_passwords(mode):
    log('info', f"Updating {mode} passwords...")

    old_psw = TMP_PASSWORD if mode == 'TMP' else RECOVERY_PSW
    _update_password_tmp() if mode == 'TMP' else _update_password_recovery()

    with APP.app_context():
        user.update_passwords(old_psw, mode)


def _updater():
    timer = _remaining_seconds()
    date = datetime.now().date()
    session_update_counter = 0
    recovery_update_counter = 0

    log('info', f"Database updater started, next update in {timer} seconds.")

    _update_password_tmp()
    _update_password_recovery()

    while True:
        time.sleep(30)
        timer -= 30
        session_update_counter += 1
        recovery_update_counter += 1

        _update_passwords('TMP')

        if timer <= 0:
            _update_users(date)
            timer = _calc_seconds(ONE_DAY)
            date += timedelta(days=1)

        if session_update_counter >= 10:
            _clear_sessions()
            session_update_counter = 0

        if recovery_update_counter >= 120:
            _update_passwords('RECOVERY')
            recovery_update_counter = 0


def start_updater():
    threading.Thread(target=_updater).start()
