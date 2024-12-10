from dotenv import load_dotenv
from pathlib import Path
from updater import updater
import subprocess
import os

def main():
    env_path = Path(__file__).resolve().parent / 'server.env'
    load_dotenv(dotenv_path=env_path)
    exec_mode = os.getenv('EXEC_MODE')

    if exec_mode == 'DEBUG':
        print("Server running in debug mode.")
        updater()
        subprocess.run(['watchmedo', 'auto-restart', '--', 'gunicorn', '-b', '127.0.0.1:5000', '-k', 'eventlet', 'app:app'])

    else:
        print("Server running in production mode.")
        subprocess.run(['gunicorn', '-b', '127.0.0.1:5000', '-k', 'eventlet', 'app:app'])


if __name__ == '__main__':
    main()
