import argparse
from PIL import Image, ImageSequence

size = (16, 16)

rows = 11
cols = 15

offset_x = 10
offset_y = 37

start_offset = 14

def main(args):
    im = Image.open(args.file)
    frames = [frame.convert('RGB') for frame in ImageSequence.Iterator(im)]

    gif = []
    bbox = (offset_x, offset_y, offset_x + 16, offset_y + 16)
    for i, frame in enumerate(frames):
        f = frame.crop(bbox).convert('RGBA')
        f.info['transparency'] = 0
        f.save('test-{0}.gif'.format(i), mode='gif')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--file', help='path to gif to process')
    parser.add_argument('-d', '--dir', help='output directory')

    args = parser.parse_args()
    main(args)
