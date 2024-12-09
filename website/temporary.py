import time
import threading
import random
from . import APP
from .logic.updating import user
from datetime import datetime, timedelta

ONE_DAY = "01:00:00:00"
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


def _remaining_seconds():
    now = datetime.now()
    end_of_day = datetime.combine(now.date(), datetime.max.time())
    remaining = end_of_day - now

    return int(remaining.total_seconds())


def _updater():
    timer = _remaining_seconds()
    date = datetime.now().date()
    date_strf = date.strftime('%d.%m.%Y')

    print(f"[{date_strf}] Updater started.")
    print(f"[{date_strf}] Next update in {timer} seconds.")

    while True:
        timer -= 1
        time.sleep(1)

        if timer <= 0:
            print(f"[{date_strf}] Updating database.")

            with APP.app_context():
                user.update(date)

            timer = _calc_seconds(ONE_DAY)
            date += timedelta(days=1)
            date_strf = date.strftime('%d.%m.%Y')


def start_updater():
    thread = threading.Thread(target=_updater)
    thread.start()
    return thread
