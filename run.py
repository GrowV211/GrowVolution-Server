from dotenv import load_dotenv
from pathlib import Path
from watcher import start_watching
from datetime import datetime
import subprocess
import threading
import time
import os

FILE_PATH = Path(__file__).resolve().parent
LOG_PATH = FILE_PATH / 'website' / 'logs'
SESSION_LOG = ''

GUNICORN_CMD = ['env', 'PYTHONUNBUFFERED=1', 'gunicorn', '-b', '127.0.0.1:5000', '-k', 'eventlet', 'app:app']
DUMMY_CMD = ['gunicorn', '-b', '127.0.0.1:5000', 'dummy:app']
PROCESS = None
LOGGER = None

EXEC_MODE = ''

EXIT = False

os.makedirs(LOG_PATH, exist_ok=True)


def start_server():
    return subprocess.Popen(GUNICORN_CMD, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, bufsize=1)


def _start_dummy():
    return subprocess.Popen(DUMMY_CMD, stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)


def start_dummy():
    print("Starting dummy server...")
    dummy = _start_dummy()
    print("Dummy server running.\n")
    return dummy


def is_debug():
    return EXEC_MODE == 'DEBUG'


def clear_logs():
    logs = FILE_PATH / 'website' / 'logs'

    print("Clearing log folder...")

    for file in logs.iterdir():
        if file.is_file():
            print(f"Deleting {file}...")
            file.unlink()
        else:
            print(f"Skipping {file} (not a file)...")

    print("\nLog folder cleared.\n")


def console():
    global LOGGER

    info = ("You can enter the following commands:"
          "\n\n\t1. start - to start the main server"
          "\n\t2. stop - to stop the main server"
          "\n\t3. restart - to restart the main server"
          "\n\t4. clear-logs - to clear the log folder"
          "\n\t5. clear - to clear the console"
          "\n\n\t6. start-dummy - to start the dummy server"
          "\n\t7. stop-dummy - to stop the dummy server (not recommended)"
          "\n\n\t8. exit - to exit this script\n")

    print("GrowVolution 2024 - GNU General Public License\n\n"
          f"Start script running.\n")

    dummy = start_dummy()

    LOGGER = threading.Thread(target=_logger)
    LOGGER.start()

    print(info)

    while True:
        cmd = input()

        if cmd == 'start':
            stop_dummy(dummy)
            main()

        elif cmd == 'stop':
            stop("The server is not running.")
            dummy = start_dummy()

        elif cmd == 'restart':
            stop("The server was not running. Just starting it now.")
            main()

        elif cmd == 'clear-logs':
            clear_logs()

        elif cmd == 'clear':
            subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)

        elif cmd == 'start-dummy':
            stop('')
            stop_dummy(dummy)
            dummy = start_dummy()

        elif cmd == 'stop-dummy':
            stop_dummy(dummy)

        elif cmd == 'exit':
            global EXIT
            EXIT = True
            stop()
            stop_dummy(dummy)
            LOGGER.join()
            print("Thank you for playing the game of life, bye!")
            break

        else:
            print(f"Unknown command.\n{info}")


def stop(alt=None):
    if PROCESS:
        _stop()
    elif alt:
        print(f"{alt}\n")


def stop_dummy(dummy):
    if dummy:
        print("Stopping dummy server...")
        dummy.terminate()
        dummy.wait()
        print("Dummy server stopped.\n")


def _stop():
    global PROCESS

    print("Shutting down server session...")

    if is_debug():
        PROCESS[1].stop_gunicorn()

        print("Stopping watchdog observer process...")
        PROCESS[0].stop()
        PROCESS[0].join()

    else:
        PROCESS.terminate()
        PROCESS.wait()

    PROCESS = None
    print("Server stopped.\n")


def _logger():
    debug = is_debug()

    print("Executing logger thread...\n")

    while not EXIT:
        process = PROCESS[1].process if PROCESS and debug else PROCESS

        if process:
            print(f"Starting logger for {SESSION_LOG}...")
            with open(LOG_PATH / SESSION_LOG, 'w') as log:
                for line in process.stdout:
                    if not line.startswith("[FLASK]"):
                        line = f"[GUNICORN] {line}"

                    if debug:
                        print(line, end='')

                    log.write(line)

            print(f"Logger for {SESSION_LOG} stopped.\n")
            time.sleep(3)

        time.sleep(1)

    print("Logger thread stopped.\n")


def main():
    global SESSION_LOG, PROCESS
    SESSION_LOG = f'SESSION-{datetime.now().strftime("%Y%m%d%H%M%S")}.log'

    print(f"Starting server in {EXEC_MODE} mode...")
    PROCESS = start_watching(start_server) if is_debug() else start_server()


if __name__ == '__main__':
    env_path = FILE_PATH / 'server.env'
    load_dotenv(dotenv_path=env_path)
    EXEC_MODE = os.getenv('EXEC_MODE')

    console()
