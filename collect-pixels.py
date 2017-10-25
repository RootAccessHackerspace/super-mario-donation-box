import argparse
import json
import os
import shutil

from PIL import Image, ImageSequence

output_dir = 'board/json'


def main(args):
    path = lambda *a: os.path.join('gifs', args.set, *a)

    # Always start fresh
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)

    for anim in os.listdir(path()):
        if not os.path.isdir(path(anim)):
            continue

        frame_list = filter(
            lambda p: p.endswith('.png'),
            os.listdir(path(anim))
        )

        for i, name in enumerate(frame_list):
            im = Image.open(path(anim, name)).convert('RGBA')
            data = {}
            for x in range(16):
                for y in range(16):
                    rgba = im.getpixel((x, y))
                    if rgba[3] == 0:
                        continue

                    key = ':'.join(map(str, rgba[:3]))
                    data.setdefault(key, [])
                    data[key].append((x, y))
                    # # Black stays off, transparent == dark gray to show outline
                    # # if rgba == (0, 0, 0, 255):
                    # #     data[-1] = '222222'
                    # if rgba[3] == 0:
                    #     data[-1] = '444444'

            if not os.path.isdir('{0}/{1}'.format(output_dir, anim)):
                os.mkdir('{0}/{1}'.format(output_dir, anim))
            output_file = '{0}/{1}/{2}.json'.format(
                output_dir, anim, str(i).zfill(2))
            with open(output_file, 'w') as f:
                f.write(json.dumps(data))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--set', help='which gif set to process')

    args = parser.parse_args()
    main(args)
