from . import APP
from datetime import datetime


def get_time():
    return f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"


def log(category, message):
    log_str = f"[FLASK] [{get_time()}] [{category.upper()}] {message}"
    print(log_str)


def start_session():
    log('info', "Logging started.")
    log('info', f"Server is now running in {APP.config['EXEC_MODE']} mode.")
