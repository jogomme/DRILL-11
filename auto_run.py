import time

from transitions.core import State


class AutoRun(State):
    SPEED_MULTIPLIER = 2
    SIZE_MULTIPLIER = 1.5

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

    def update(self, boy, now):
        boy.x += boy.face_dir * boy.RUN_SPEED * self.SPEED_MULTIPLIER
        boy.frame = (boy.frame + 1) % 8
        return False
