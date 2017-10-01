import argparse
import os

from PIL import Image, ImageSequence

size = (16, 16)


# def main(args):
#     im = Image.open(args.file)
#     frames = [frame.convert('RGB') for frame in ImageSequence.Iterator(im)]

#     for i, frame in enumerate(frames):
#         data = []
#         frame.thumbnail(size)
#         for x in range(16):
#             for y in range(16):
#                 data.append(''.join(
#                     [hex(b)[2:].zfill(2) for b in frame.getpixel((x, y))]
#                 ))
#                 if data[-1] == 'ffffff':
#                     data[-1] = '000000'

#         with open('{0}/{1}.txt'.format(args.dir, str(i).zfill(2)), 'w') as f:
#             f.write(','.join(data))

def main(args):
    frames = []
    for i, name in enumerate(filter(lambda p: p.endswith('.png'), os.listdir(args.file))):
        im = Image.open('{0}/{1}'.format(args.file, fname))
        data = []
        for x in range(16):
            for y in range(16):
                data.append(''.join(
                    [hex(b)[2:].zfill(2) for b in frame.getpixel((x, y))]
                ))
                if data[-1] == 'ffffff':
                    data[-1] = '000000'

        with open('{0}/{1}.txt'.format(args.dir, str(i).zfill(2)), 'w') as f:
            f.write(','.join(data))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--file', help='path to gif to process')
    parser.add_argument('-d', '--dir', help='output directory')

    args = parser.parse_args()
    main(args)
