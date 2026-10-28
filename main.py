from pico2d import *
import random

from grass import Grass
from boy import Boy


# Game object class here

def handle_events():
    global running, pressed_directions

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if boy.state == 'SLEEP':
                boy.wake()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            if boy.state == 'IDLE':
                boy.start_auto_run()
        elif event.type == SDL_KEYDOWN and event.key in (SDLK_LEFT, SDLK_RIGHT):
            if event.key not in pressed_directions:
                pressed_directions.append(event.key)
        elif event.type == SDL_KEYUP and event.key in (SDLK_LEFT, SDLK_RIGHT):
            if event.key in pressed_directions:
                pressed_directions.remove(event.key)

    if pressed_directions:
        direction = 1 if pressed_directions[-1] == SDLK_RIGHT else -1
        if boy.state in ('IDLE', 'SLEEP'):
            boy.start_run(direction=direction)
        elif boy.state == 'RUN':
            boy.set_direction(direction)
        elif boy.state == 'AutoRun':
            boy.interrupt_auto_run(direction=direction)
    elif boy.state == 'RUN':
        boy.stop_run()


def reset_world():
    global world, pressed_directions
    global boy

    world = []
    pressed_directions = []

    grass = Grass()
    world.append(grass)

    boy = Boy()
    world.append(boy)



def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


running = True


def run():
    global running

    running = True
    open_canvas()
    try:
        reset_world()
        while running:
            handle_events()
            update_world()
            render_world()
            delay(0.01)
    finally:
        close_canvas()


if __name__ == '__main__':
    run()
