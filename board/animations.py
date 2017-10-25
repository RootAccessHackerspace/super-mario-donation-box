import random
import time

from graphics import FrameSequence

animation_list = []

def animation(fn):
    animation_list.append(fn)
    return fn


@animation
def star(matrix):
    frame = FrameSequence('star').first_frame()
    x_path = range(-16, 16)
    y_path = list(range(-12, 4)) + list(sorted(range(-12, 3), reverse=True))
    path = zip(x_path, y_path)
    for x, y in path:
        frame.render(matrix, x, y)


@animation
def mario(matrix):
    walking = FrameSequence('mario-walking').cycle()
    standing = FrameSequence('mario-stand').first_frame()

    # Mario walks on screen
    x_path = range(-16, 0)
    for x in x_path:
        next(walking).render(matrix, x_offset=x)

    standing.render(matrix)
    time.sleep(1)

    if random.choice((True, False)):
        # Might as well jump (jump!)
        jump = FrameSequence('mario-jump').first_frame()
        y_path = [-1, -2, -3, -4, -3, -2, -1]
        for y in y_path:
            jump.render(matrix, y_offset=y)

        # Exit stage left
        x_path = range(16)
        for x in x_path:
            next(walking).render(matrix, x_offset=x)
    else:
        # He's dead, Jim
        dead = FrameSequence('mario-dead').first_frame()
        y_path = [0, 0, -1, -2, -3, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        for y in y_path:
            dead.render(matrix, y_offset=y)


@animation
def goomba(matrix):
    frames = FrameSequence('goomba').cycle()
    x_path = sorted(range(-16, 16), reverse=True)
    for x in x_path:
        next(frames).render(matrix, x_offset=x)


@animation
def koopa_troopa(matrix):
    frames = FrameSequence('koopa-troopa').cycle()
    x_path = sorted(range(-16, 16), reverse=True)
    for x in x_path:
        next(frames).render(matrix, x_offset=x)


@animation
def bullet_biff(matrix):
    frames = FrameSequence('bullet-biff').cycle()
    x_path = sorted(range(-16, 16), reverse=True)
    for x in x_path:
        next(frames).render(matrix, x_offset=x)


@animation
def mushroom(matrix):
    shroom = 'mushroom-{0}'.format(random.choice((
        '1-up', 'poison', 'super-og', 'super-red',
    )))
    frames = FrameSequence(shroom).cycle()
    x_path = range(-16, 16)
    for x in x_path:
        next(frames).render(matrix, x_offset=x)


@animation
def piranha_plant(matrix):
    plant = FrameSequence('piranha-plant')
    frame = plant.first_frame()
    y_path = sorted(range(17), reverse=True)
    for y in y_path:
        frame.render(matrix, y_offset=y)

    for frame in plant.get_frames(repeat=5):
        frame.render(matrix)
    frame.render(matrix)
