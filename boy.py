import math
import time

from pico2d import load_image
from transitions import Machine

from auto_run import AutoRun


class Boy:
    CANVAS_WIDTH = 800
    HALF_WIDTH = 50
    RUN_SPEED = 5

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.image = load_image('animation_sheet.png')
        self.idle_started_at = time.monotonic()
        self.machine = Machine(
            model=self,
            states=['IDLE', 'RUN', 'SLEEP', AutoRun(name='AutoRun')],
            initial='IDLE',
            auto_transitions=False,
            transitions=[
                {
                    'trigger': 'sleep',
                    'source': 'IDLE',
                    'dest': 'SLEEP',
                },
                {
                    'trigger': 'wake',
                    'source': 'SLEEP',
                    'dest': 'IDLE',
                    'after': '_reset_idle_timer',
                },
                {
                    'trigger': 'start_auto_run',
                    'source': 'IDLE',
                    'dest': 'AutoRun',
                },
                {
                    'trigger': 'start_run',
                    'source': ['IDLE', 'SLEEP'],
                    'dest': 'RUN',
                    'before': '_set_direction',
                },
                {
                    'trigger': 'stop_run',
                    'source': 'RUN',
                    'dest': 'IDLE',
                    'after': '_reset_idle_timer',
                },
            ],
        )

    def update(self):
        if self.state == 'IDLE':
            if time.monotonic() - self.idle_started_at >= 5:
                self.sleep()
                return
        if self.state == 'AutoRun':
            self.machine.get_state('AutoRun').update(self, time.monotonic())
            return
        if self.state == 'RUN':
            self.x = max(
                self.HALF_WIDTH,
                min(self.CANVAS_WIDTH - self.HALF_WIDTH,
                    self.x + self.face_dir * self.RUN_SPEED),
            )
        if self.state in ('IDLE', 'RUN', 'SLEEP'):
            self.frame = (self.frame + 1) % 8

    def _set_direction(self, direction):
        self.face_dir = direction
        self.frame = 0

    def set_direction(self, direction):
        self.face_dir = direction

    def _reset_idle_timer(self):
        self.idle_started_at = time.monotonic()
        self.frame = 0

    def draw(self):
        if self.state in ('RUN', 'AutoRun'):
            row = 100 if self.face_dir == 1 else 0
            draw_size = 100
            if self.state == 'AutoRun':
                draw_size = int(
                    100 * self.machine.get_state('AutoRun').SIZE_MULTIPLIER
                )
            self.image.clip_draw(
                self.frame * 100, row, 100, 100, self.x, self.y,
                draw_size, draw_size,
            )
            return

        if self.state == 'SLEEP':
            row = 300 if self.face_dir == 1 else 200
            angle = math.pi / 2 if self.face_dir == 1 else -math.pi / 2
            self.image.clip_composite_draw(
                self.frame * 100, row, 100, 100, angle, '',
                self.x, self.y - 20, 100, 100,
            )
            return

        if self.face_dir == 1:
            self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)
