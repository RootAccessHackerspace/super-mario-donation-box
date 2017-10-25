import gc
import machine
import neopixel
import os
import ujson


def gpath(*args):
    path = ['json']
    path.extend(args)
    return '/'.join(path)


class PixelMatrix(object):
    transparent = (4, 4, 4)

    def __init__(self, pin, width, height, serpentine=True, autofill=True):
        self.width = width
        self.height = height
        self.serpentine = serpentine
        self.pin = machine.Pin(pin)
        self.np = neopixel.NeoPixel(self.pin, self.width * self.height)

        if autofill:
            self.fill()
            self.write()

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


class FrameSequence(object):
    def __init__(self, name):
        self.name = name

    @property
    def frame_list(self):
        return os.listdir(gpath(self.name))

    def get_frames(self, repeat=1):
        for x in range(repeat):
            for frame in self.frame_list:
                yield Frame(gpath(self.name, frame))

    def cycle(self):
        while True:
            yield from self.get_frames()

    def first_frame(self):
        return next(self.get_frames())


class Frame(object):
    def __init__(self, path):
        self.path = path

    def check_position(self, n, max):
        return (n >= 0) and (n < max)

    def pixels(self):
        data = ujson.loads(open(self.path).read())
        for key, coords in data.items():
            rgb = tuple(map(lambda x: int(float(x) * .1), key.split(':')))
            yield rgb, coords
        del data
        gc.collect()

    def render(self, matrix, x_offset=0, y_offset=0, fill=True):
        if fill:
            matrix.fill()
        for rgb, coords in self.pixels():
            for (x, y) in coords:
                x += x_offset
                y += y_offset
                if not self.check_position(x, matrix.width) or not self.check_position(y, matrix.height):
                    continue
                matrix[(x, y)] = rgb
        matrix.write()
        gc.collect()
