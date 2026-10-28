import time

from transitions.core import State


class AutoRun(State):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.started_at = None

    def enter(self, event_data):
        super().enter(event_data)
        self.started_at = time.monotonic()
        event_data.model.frame = 0

    def exit(self, event_data):
        super().exit(event_data)
        self.started_at = None
