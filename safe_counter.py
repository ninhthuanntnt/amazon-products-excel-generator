import threading


class SafeCounter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._value += 1

    def plus(self, value):
        with self._lock:
            self._value += value

    def decrement(self):
        with self._lock:
            self._value -= 1

    def value(self):
        with self._lock:
            return self._value