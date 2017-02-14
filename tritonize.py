import numpy as np
import argparse
import os
from scipy.misc import toimage
from scipy.ndimage import imread, gaussian_filter
from itertools import permutations

colors = ['#1a1a1a', '#FFFFFF', (44, 62, 80)]


def hex_to_rgb_triplet(triplet):
    # http://stackoverflow.com/a/4296727
    triplet = triplet.lstrip('#')
    _NUMERALS = '0123456789abcdefABCDEF'
    _HEXDEC = {v: int(v, 16)
               for v in (x + y for x in _NUMERALS for y in _NUMERALS)}
    return _HEXDEC[triplet[0:2]], _HEXDEC[triplet[2:4]], _HEXDEC[triplet[4:6]]


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


def create_tritone(image_path, colors):
    colors_triplets = [hex_to_rgb_triplet(color) if isinstance(
        color, str) else color for color in colors]

    color_list = list(permutations(colors_triplets))

    im = imread(image_path, mode='L')

    im = np.asarray(im).copy()
    # blur_px_per_mp = 0.25
    # blur = im.size / (blur_px_per_mp * 1000000)
    # gaussian_filter(im, output=im, sigma=blur)

    threshold_matrix = sigmoid(im)
    base_name = os.path.splitext(os.path.basename(image_path))[0]

    # Create directory to store the images
    if not os.path.exists('tritonize'):
        os.makedirs('tritonize')

    for i, color_set in enumerate(color_list):
        im_color = color_select(threshold_matrix, color_set)

        imfile = toimage(im_color, mode='RGB')
        imfile.save("tritonize/{}_{}.png".format(base_name, i + 1))

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(
    #     description='Tritonize - Convert Images to a minimal representation \
    #     quickly with numpy')
    # parser.add_argument('image',  help='Image file name')
    # parser.add_argument(
    #     '--colors', type=list, nargs='+',
    #     help='List of colors (either RGB triplets or Hex strings)')

    # args = parser.parse_args()
    #create_tritone(args.image, args.colors)
    create_tritone('profile_old.png', ['#1a1a1a', '#FFFFFF', (44, 62, 80)])
