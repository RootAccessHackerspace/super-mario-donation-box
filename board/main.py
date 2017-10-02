import gc
import machine
import neopixel
import os
import ujson

import itertools

from nodemcu import PinMap

gc.collect()

animations = (
    'block',
    'bricks',
    'bullet-biff',
    'coin',
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
    'piranha-plant',
    'star',
)


class PixelMatrix(object):
    transparent = (4, 4, 4)

    def __init__(self, pin, width, height, serpentine=True):
        self.width = width
        self.height = height
        self.serpentine = serpentine
        self.np = neopixel.NeoPixel(PinMap.pin(pin), self.width * self.height)

    def __setitem__(self, index, value):
        if isinstance(index, tuple):
            index = self.XY(*index)
        self.np[index] = value

    def fill(self, color=None):
        return self.np.fill(color or self.transparent)

    def write(self):
        return self.np.write()

    # XY conversion taken from FastLED/XYMatrix
    def XY(self, x, y):
        if self.serpentine is False:
            return (y * self.width) + x
        if(y % 2 != 0):
            reverse_x = (self.width - 1) - x
            return (y * self.width) + reverse_x
        return (y * self.width) + x


# class Animation(object):
#     def __init__(self, name):
#         self.name = name


# class Frame(object):
#     def __init__(self, name, num):
#         self.name =


matrix = PixelMatrix('D2', 16, 16)

def load_frame(frame):
    data = ujson.loads(open(frame).read())
    for key, coords in data.items():
        rgb = tuple(map(lambda x: int(float(x) * .1), key.split(':')))
        yield rgb, coords
    del data
    gc.collect()


def draw_frame(data):
    matrix.fill()
    for rgb, coords in data:
        for (x, y) in coords:
            matrix[(x, y)] = rgb
    matrix.write()
    gc.collect()

def gpath(*args):
    path = ['json']
    path.extend(args)
    return '/'.join(path)

def loop():
    for anim in animations:
        for x in range(5):
            for frame in os.listdir(gpath(anim)):
                draw_frame(
                    load_frame(
                        gpath(anim, frame)
                    )
                )
                gc.collect()

while True:
    loop()
