import datetime
import logging
import threading
import time


class SafeRandomGenerator:
    def __init__(self):
        self._lock = threading.Lock()

    def generate_from_datetime(self) -> str:
        with self._lock:
            time.sleep(1)
            logging.info("Delay 1 second")
            now = datetime.datetime.now()
            current_datetime = now.strftime("%d%m%Y-%H%M%S")
            return current_datetime;

    def generate_from_milisecond(self) -> str:
        with self._lock:
            time.sleep(0.1)
            logging.info("Delay 0.1 second")
            current_datetime = str(round(time.time() * 1000))
            return current_datetime;

generator = SafeRandomGenerator()

