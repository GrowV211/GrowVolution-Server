from . import APP
from datetime import datetime
from pathlib import Path
import os

LOG_PATH = Path(__file__).resolve().parent / 'logs'
SESSION_LOG = ''

os.makedirs(LOG_PATH, exist_ok=True)


def get_time():
    return f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"


def log(category, message):
    log_str = f"[{get_time()}] [{category.upper()}] {message}"

    if APP.config['EXEC_MODE'] == 'DEBUG':
        print(log_str)

    write_log(f'{log_str}\n')


def write_log(log_str):
    with open(LOG_PATH / SESSION_LOG, 'a') as f:
        f.write(log_str)


def start_session():
    global SESSION_LOG

    SESSION_LOG = f'SESSION-{datetime.now().strftime("%Y%m%d%H%M%S")}.log'

    log('info', "Logging started.")
    log('info', f"Server is now running in {APP.config['EXEC_MODE']} mode.")
