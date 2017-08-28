import numpy as np
import argparse
import os
from scipy.misc import *
from scipy.ndimage import *
from itertools import permutations
from ast import literal_eval as make_tuple
from PIL import Image


def string_to_rgb_triplet(triplet):

    if '#' in triplet:
        # http://stackoverflow.com/a/4296727
        triplet = triplet.lstrip('#')
        _NUMERALS = '0123456789abcdefABCDEF'
        _HEXDEC = {v: int(v, 16)
                   for v in (x + y for x in _NUMERALS for y in _NUMERALS)}
        return (_HEXDEC[triplet[0:2]], _HEXDEC[triplet[2:4]],
                _HEXDEC[triplet[4:6]], 255)

    else:
        # https://stackoverflow.com/a/9763133
        triplet = make_tuple(triplet)
        return triplet + (255,) if len(triplet) == 3 else triplet


def sigmoid(x):

    # result is between 0 and 1
    # since values between 0 and 255, (x-128)/32.0) converts range to about
    # (-4.0, 4.0)

    threshold_matrix = 1.0 / (1.0 + np.exp(-((x - 128.0) / 32.0)))
    return threshold_matrix


def color_select(threshold_matrix, colors):

    # Takes a matrix of thresholds and returns a matrix of correpsonding colors

    indices_matrix = (threshold_matrix * len(colors)).astype(int)
    return np.array(colors)[indices_matrix]


def create_tritone(image_path, colors, blur, bg_color):
    colors_triplets = [string_to_rgb_triplet(color) if isinstance(
        color, str) else color for color in colors]

    color_list = list(permutations(colors_triplets))

    im = imread(image_path, mode='L')

    im = np.asarray(im).copy()
    blur_px_per_mp = blur
    blur = im.size * blur_px_per_mp / (1000000)
    gaussian_filter(im, output=im, sigma=blur)

    threshold_matrix = sigmoid(im)
    base_name = os.path.splitext(os.path.basename(image_path))[0]

    background = Image.new('RGBA', im.shape, make_tuple(bg_color))

    # Create directory to store the images
    if not os.path.exists('tritonize'):
        os.makedirs('tritonize')

    for i, color_set in enumerate(color_list):
        im_color = color_select(threshold_matrix, color_set)

        imfile = toimage(im_color, mode='RGBA')

        merged = Image.alpha_composite(background, imfile)
        merged.save("tritonize/{}_{}.png".format(base_name, i + 1))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Tritonize - Convert images to a styled, minimal  \
        representation quickly with NumPy')
    parser.add_argument('-i', '--image',  help='Image file name',
                        required=True)
    parser.add_argument('-c',
                        '--colors', nargs='+',
                        help='List of colors (as HEX strings or '
                        '3/4-element tuple strings)', required=True)
    parser.add_argument('-b',
                        '--blur', nargs='?', default=4.0, type=float,
                        help='Blur strength')
    parser.add_argument('-bg',
                        '--background', nargs='?', default="(0, 0, 0, 0)",
                        help='Background color (for transparent images)')

    args = parser.parse_args()
    create_tritone(args.image, args.colors, args.blur, args.background)
