import gc
import time
import random

import itertools

from animations import animation_list
from graphics import PixelMatrix, FrameSequence
from nodemcu import PinMap
from sensors import HCSR04

gc.collect()

image_list = (
    'block',
    'bricks',
    'bullet-biff',
    'coin',
    'explosion',
    'fire-flower',
    'goomba',
    'heart',
    'koopa-troopa',
    'mario-walking',
    'mushroom-1-up',
    'mushroom-poison',
    'mushroom-super-og',
    'mushroom-super-red',
    'mushroom-warhol',
    'pipe',
    'piranha-plant',
    'star',
)

# Define our pins
matrix = PixelMatrix(PinMap.D2, 16, 16)
sonar = HCSR04(PinMap.D1)

# Reset the matrix
matrix.fill()
matrix.write()

# Default block image
block = FrameSequence('block').first_frame()
block.render(matrix)


def loop():
    ping = sonar.ping()
    if ping > 0:
        distance = sonar.convert_cm(ping)
        if distance < 5:
            time.sleep(2)

            # Slide the block down
            path = [(0, y) for y in range(1, 17)]
            for (x, y) in path:
                block.render(matrix, x, y)

            # Spin the coin a couple times
            sequence = FrameSequence('coin')
            for frame in sequence.get_frames(repeat=4):
                frame.render(matrix)
            sequence.first_frame().render(matrix)
            time.sleep(1)

            # Make something walk across the screen, then return to the block.
            random.choice(animation_list)(matrix)
            block.render(matrix)
        time.sleep(0.1)


while True:
    loop()
