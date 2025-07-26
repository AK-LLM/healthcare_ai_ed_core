import threading

class AppContext:
    """
    Central context for inter-module data.
    Thread-safe, modular, with audit hooks.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self.state = {}
        # Initialize slots for each module as needed (e.g., triage, flow, etc.)

    def set(self, key, value):
        with self._lock:
            self.state[key] = value
            # Call audit log if needed

    def get(self, key, default=None):
        with self._lock:
            return self.state.get(key, default)

    def clear(self):
        with self._lock:
            self.state.clear()

# Singleton for use throughout app
context = AppContext()
