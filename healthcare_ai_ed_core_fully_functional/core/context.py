
import threading
class AppContext:
    def __init__(self):
        self._lock = threading.Lock()
        self.state = {}
    def set(self, key, value):
        with self._lock:
            self.state[key] = value
    def get(self, key, default=None):
        with self._lock:
            return self.state.get(key, default)
    def clear(self):
        with self._lock:
            self.state.clear()
context = AppContext()
