import time
import threading
import random
from . import APP, SOCKET
from .debugger import log
from .logic.updating import user
from .logic.socket.manage import send_message
from datetime import datetime, timedelta

ONE_DAY = "01:00:00:00"
ONE_HOUR = "00:01:00:00"
TEN_MINUTES = "00:00:10:00"

CONFIRM = {}
LOCK = {}
TIMES_LOCKED = {}

RESET = {}

STOPPED = False


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


def _clear_session(session_id):
    from .data import Session, delete_model
    session = Session.query.filter_by(id=session_id).first()
    sid = session.sid
    if sid:
        send_message('reload', None, sid)
        SOCKET.disconnect(sid)
    delete_model(session)


def _session_cycle(session_id):
    seconds = _calc_seconds(ONE_HOUR) + 2
    time.sleep(seconds)
    _clear_session(session_id)


def session_lifecycle(session_id):
    threading.Thread(target=_session_cycle, args=(session_id,)).start()


def _remaining_seconds():
    now = datetime.now()
    end_of_day = datetime.combine(now.date(), datetime.max.time())
    remaining = end_of_day - now

    return int(remaining.total_seconds())


def _updater():
    timer = _remaining_seconds()
    date = datetime.now().date()

    log('info', f"Database updater started, next update in {timer} seconds.")

    while True:
        time.sleep(timer)

        log('info', "Updating database.")

        with APP.app_context():
            user.update(date)

        timer = _calc_seconds(ONE_DAY)
        date += timedelta(days=1)


def start_updater():
    threading.Thread(target=_updater).start()
