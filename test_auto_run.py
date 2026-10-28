import unittest
from types import SimpleNamespace
from unittest.mock import patch

import main as game
from boy import Boy


class FakeImage:
    def __init__(self):
        self.draw_calls = []

    def clip_draw(self, *args):
        self.draw_calls.append(args)

    def clip_composite_draw(self, *args):
        self.draw_calls.append(args)


class AutoRunTests(unittest.TestCase):
    def setUp(self):
        self.image_patcher = patch(
            'boy.load_image', side_effect=lambda _: FakeImage()
        )
        self.image_patcher.start()
        self.addCleanup(self.image_patcher.stop)
        self.boy = Boy()
        game.boy = self.boy
        game.pressed_directions = []
        game.running = True

    def send_key(self, event_type, key):
        event = SimpleNamespace(type=event_type, key=key)
        with patch.object(game, 'get_events', return_value=[event]):
            game.handle_events()

    def test_a_starts_auto_run_only_from_idle(self):
        self.send_key(game.SDL_KEYDOWN, game.SDLK_a)
        self.assertEqual(self.boy.state, 'AutoRun')

        self.boy = Boy()
        self.boy.start_run(direction=1)
        game.boy = self.boy
        self.send_key(game.SDL_KEYDOWN, game.SDLK_a)
        self.assertNotEqual(self.boy.state, 'AutoRun')
        self.boy.sleep()
        self.send_key(game.SDL_KEYDOWN, game.SDLK_a)
        self.assertEqual(self.boy.state, 'SLEEP')

    def test_direction_key_interrupts_auto_run_and_preserves_run_input(self):
        self.boy.start_auto_run()
        self.send_key(game.SDL_KEYDOWN, game.SDLK_LEFT)
        self.assertEqual(self.boy.state, 'RUN')
        self.assertEqual(self.boy.face_dir, -1)
        self.boy.update()
        self.assertEqual(self.boy.x, 395)

    def test_auto_run_speed_size_and_bounds(self):
        self.boy.start_auto_run()
        self.boy.update()
        self.assertEqual(self.boy.x, 410)
        self.boy.draw()
        self.assertEqual(self.boy.image.draw_calls[-1][-2:], (150, 150))

        self.boy.x = 740
        self.boy.face_dir = 1
        self.boy.update()
        self.assertEqual(self.boy.x, 725)
        self.assertEqual(self.boy.face_dir, -1)
        self.boy.x = 80
        self.boy.face_dir = -1
        self.boy.update()
        self.assertEqual(self.boy.x, 75)
        self.assertEqual(self.boy.face_dir, 1)

    def test_timeout_returns_to_idle_at_five_seconds(self):
        auto_run = self.boy.machine.get_state('AutoRun')
        with patch('auto_run.time.monotonic', return_value=100):
            self.boy.start_auto_run()
        with patch('boy.time.monotonic', return_value=104.999):
            self.boy.update()
        self.assertEqual(self.boy.state, 'AutoRun')
        position_before_expiry = self.boy.x
        with patch('boy.time.monotonic', return_value=105):
            self.boy.update()
        self.assertEqual(self.boy.state, 'IDLE')
        self.assertEqual(self.boy.x, position_before_expiry)
        self.assertEqual(self.boy.idle_started_at, 105)
        self.assertIsNone(auto_run.started_at)

    def test_existing_run_release_and_sleep_wake_inputs(self):
        self.send_key(game.SDL_KEYDOWN, game.SDLK_RIGHT)
        self.assertEqual(self.boy.state, 'RUN')
        self.send_key(game.SDL_KEYUP, game.SDLK_RIGHT)
        self.assertEqual(self.boy.state, 'IDLE')

        self.boy.sleep()
        self.send_key(game.SDL_KEYDOWN, game.SDLK_SPACE)
        self.assertEqual(self.boy.state, 'IDLE')

    def test_escape_and_window_close_still_stop_game(self):
        self.send_key(game.SDL_KEYDOWN, game.SDLK_ESCAPE)
        self.assertFalse(game.running)
        game.running = True
        self.send_key(game.SDL_QUIT, 0)
        self.assertFalse(game.running)


if __name__ == '__main__':
    unittest.main()
