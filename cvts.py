import argparse
import os

from PIL import Image, ImageDraw, ImageFont
import sys


def list_dir(path='.', dir_only=True, file_only=False):
    files = os.listdir(path)
    dirs = []
    for name in files:
        # print(name)

        full_path = os.path.join(path, name)
        # print(full_path)

        if dir_only and os.path.isdir(full_path):
            dirs.append(name)
            pass
        if file_only and os.path.isfile(full_path):
            dirs.append(name)
            pass
    return dirs
    pass


def recursive_image_gen(path, filter=()):
    if os.path.isdir(path):
        # get file list
        files = list_dir(path=path, dir_only=False, file_only=True)
        # loop over files and generate image
        for f in files:
            gen_image(os.path.join(path, f))
            pass
        # get directory list
        sub_dirs = list_dir(path=path, dir_only=True, file_only=False)
        # loop over dirs and generate image
        for d in sub_dirs:
            recursive_image_gen(os.path.join(path, d))
    else:
        gen_image(path)
        pass
    pass


def gen_image(file_name):
    try:
        # open the file
        with open(file_name) as fp:
            # read all lines
            lines = fp.readlines()

            max = 0
            # find the maximum line length
            for l in lines:
                if len(l) > max:
                    max = len(l)
                pass
            line_no_digits = 4
            # create image with white BG . image width 10 * max, height = 19 * no of lines
            img = Image.new('RGB', (10 * max + line_no_digits, 19 * len(lines)), color=(255, 255, 255))
            fnt = ImageFont.truetype('NotoMono-Regular.ttf', 15)
            d = ImageDraw.Draw(img)

            y = 5
            line_height = 18
            ctr = 1
            fmt = "{:" + f"{line_no_digits}" + "d}"
            for l in lines:
                l = l.replace("\t", '   ')
                line_no = fmt.format(ctr)
                d.text((5, y), f"{line_no} {l}\n", font=fnt, fill=(0, 0, 0))
                y += line_height
                ctr += 1
                pass
            dd = os.path.split(file_name)
            img.save(f'{dd[0]}/{dd[1]}.png')
            print(f"Image Generated: {dd[0]}/{dd[1]}.png")
            pass
        pass
    except Exception as e:
        print(f"unable to open file : {file_name}",)
        print(e)
        pass


if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dir", type=str, required=True,
                    help="path to input files")
    ap.add_argument("-f", "--filter", type=str, required=True,
                    help="file extension filter")
    args = vars(ap.parse_args())

    root = args['dir']
    filters = args['filter']
    recursive_image_gen(root, filters)
    pass
