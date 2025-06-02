import sys
import time
from threading import Thread
import itertools
import os

class ProgressBar:
    def __init__(self, total, description="Processing"):
        self.total = total
        self.description = description
        self.current = 0
        self.start_time = time.time()
        self.spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        self.spinner_thread = None
        self.running = False

    def _spinner_animation(self):
        while self.running:
            sys.stdout.write(f"\r{next(self.spinner)} {self.description}... ")
            sys.stdout.flush()
            time.sleep(0.1)

    def start(self):
        self.running = True
        self.spinner_thread = Thread(target=self._spinner_animation)
        self.spinner_thread.start()

    def update(self, value):
        self.current = value
        elapsed = time.time() - self.start_time
        progress = self.current / self.total
        bar_length = 40
        filled_length = int(bar_length * progress)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        eta = (elapsed / progress) - elapsed if progress > 0 else 0
        sys.stdout.write(f"\r{bar} {progress:.1%} | {self.current}/{self.total} | ETA: {eta:.1f}s")
        sys.stdout.flush()

    def stop(self):
        self.running = False
        if self.spinner_thread:
            self.spinner_thread.join()
        elapsed = time.time() - self.start_time
        sys.stdout.write(f"\r{' ' * (os.get_terminal_size().columns - 1)}\r")
        sys.stdout.write(f"✓ Completed in {elapsed:.1f}s\n")
        sys.stdout.flush()

def clear_line():
    sys.stdout.write("\r" + " " * (os.get_terminal_size().columns - 1) + "\r")
    sys.stdout.flush() 