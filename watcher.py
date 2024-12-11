from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

PROJECT_PATH = Path(__file__).resolve().parent

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, starter):
        self.process = None
        self.starter = starter

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f"Changes detected: {event.src_path}")
            self.restart_gunicorn()

    def on_created(self, event):
        if event.src_path.endswith('.py'):
            print(f"New file created: {event.src_path}")
            self.restart_gunicorn()

    def start_gunicorn(self):
        self.process = self.starter()

    def restart_gunicorn(self):
        print("Shutting down current session...")
        self.stop_gunicorn()
        print("Starting new session...")
        self.start_gunicorn()

    def stop_gunicorn(self):
        if self.process:
            self.process.terminate()
            self.process.wait()


def start_watching(starter):
    event_handler = ChangeHandler(starter)
    observer = Observer()
    observer.schedule(event_handler, PROJECT_PATH, recursive=True)
    observer.start()

    print("Starting session using watchdog...")
    event_handler.start_gunicorn()

    return [observer, event_handler]

