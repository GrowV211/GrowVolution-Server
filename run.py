from dotenv import load_dotenv
from pathlib import Path
from watcher import start_watching
import subprocess
import os

FILE_PATH = Path(__file__).resolve().parent
GUNICORN_CMD = ['gunicorn', '-b', '127.0.0.1:5000', '-k', 'eventlet', 'app:app']
PROCESS = None

EXEC_MODE = ''


def start_server():
    return subprocess.Popen(GUNICORN_CMD)


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

    print("\nLog folder cleared.")


def console():
    info = ("You can enter the following commands:"
          "\n\n\t1. start - to start the server"
          "\n\t2. stop - to stop the server"
          "\n\t3. restart - to restart the server"
          "\n\t4. clear-logs - to clear the log folder"
          "\n\t5. exit - to exit this script\n")

    print("GrowVolution 2024 - GNU General Public License\n\n"
          f"Start script running.\n{info}")

    while True:
        cmd = input()

        if cmd == 'start':
            main()

        elif cmd == 'stop':
            stop("The server is not running.")

        elif cmd == 'restart':
            stop("The server was not running. Just starting it now.")
            main()

        elif cmd == 'clear-logs':
            clear_logs()

        elif cmd == 'exit':
            stop('')
            print("Thank you for playing the game of life, bye!")
            break

        else:
            print(f"Unknown command.\n{info}")


def stop(alt):
    if PROCESS:
        _stop()
    else:
        print(alt)


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
    print("Server stopped.")


def main():
    global PROCESS

    if is_debug():
        print("Starting server in debug mode.")
        PROCESS = start_watching(start_server)

    else:
        print("Starting server in production mode.")
        PROCESS = start_server()


if __name__ == '__main__':
    env_path = FILE_PATH / 'server.env'
    load_dotenv(dotenv_path=env_path)
    EXEC_MODE = os.getenv('EXEC_MODE')

    console()
