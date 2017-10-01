import gc
import machine
import neopixel
import os

gc.collect()

class PinMap(object):
    D0 = 16;
    D1 = 5;
    D2 = 4;
    D3 = 0;
    D4 = 2;
    D5 = 14;
    D6 = 12;
    D7 = 13;
    D8 = 15;
    D9 = 3;
    D10 = 1;


# class PixelMatrix(object):
#     def __init__(self, pin, width, height, serpentine=False):
#         self.width = width
#         self.height = height
#         self.serpentine = serpentine
#         self.np = neopixel.NeoPixel(machine.Pin(pin), self.width * self.height)

#     def XY(self, x, y):
#         if self.serpentine is False:
#             return (y * self.width) + x
#         if(y % 2 != 0):
#             reverse_x = (self.width - 1) - x
#             return (y * self.width) + reverse_x
#         return (y * self.width) + x


matrix_width = 16
matrix_height = 16
serpentine_layout = True

np = neopixel.NeoPixel(machine.Pin(PinMap.D2), 256)

# XY conversion taken from FastLED/XYMatrix
def XY(x, y):
    i = 0
    if serpentine_layout is False:
        i = (y * matrix_width) + x
    else:
        if(y % 2 != 0):
            reverse_x = (matrix_width - 1) - x
            i = (y * matrix_width) + reverse_x
        else:
            i = (y * matrix_width) + x
    return i


def load_frame(frame):
    data = []
    pixels = open(frame).read().split(',')
    for pixel in pixels:
        data.append((
            int(int(pixel[:2], 16) * .1),
            int(int(pixel[2:4], 16) * .1),
            int(int(pixel[4:6], 16) * .1),
        ))
    del pixels
    gc.collect()
    return data


def draw_frame(data):
    for x in range(matrix_height):
        for y in range(matrix_width):
            np[XY(x, y)] = data[(y * matrix_width) + x]
    np.write()
    gc.collect()

def gpath(*args):
    path = ['gifs']
    path.extend(args)
    return '/'.join(path)

def loop():
    for anim in os.listdir(gpath()):
        for x in range(5):
            for frame in os.listdir(gpath(anim)):
                data = load_frame(gpath(anim, frame))
                draw_frame(data)
                del data
                gc.collect()

while True:
    loop()
