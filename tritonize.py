import numpy as np
import math
from scipy.misc import toimage
from scipy.ndimage import imread, gaussian_filter
from itertools import permutations

colors = [(26, 26, 26), (255, 255, 255), (44, 62, 80)]
color_list = list(permutations(colors))
blur_px_per_mp = 0.25


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

im = imread("test/profile.png", mode='L')

im = np.asarray(im).copy()
#blur = im.size / (blur_px_per_mp * math.pow(10, 6))
#gaussian_filter(im, output=im, sigma=blur)

threshold_matrix = sigmoid(im)

for i, color_set in enumerate(color_list):
    im_color = color_select(threshold_matrix, color_set)

    imfile = toimage(im_color, mode='RGB')
    imfile.save("test/profile_color_{}.png".format(i+1))
