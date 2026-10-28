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
        half_width = boy.HALF_WIDTH * self.SIZE_MULTIPLIER
        left_edge = half_width
        right_edge = boy.CANVAS_WIDTH - half_width
        next_x = (
            boy.x
            + boy.face_dir * boy.RUN_SPEED * self.SPEED_MULTIPLIER
        )
        if next_x <= left_edge:
            boy.x = left_edge
            boy.face_dir = 1
        elif next_x >= right_edge:
            boy.x = right_edge
            boy.face_dir = -1
        else:
            boy.x = next_x
        boy.frame = (boy.frame + 1) % 8
        return False
