from PIL import Image, ImageFilter
import numpy as np
import math
from scipy.misc import toimage

colors = [(26, 26, 26), (255, 255, 255), (44, 62, 80)]
blur_px_per_mp = 1


def sigmoid(x):

    # result is between 0 and 1
    # since values between 0 and 255, (x-128)/32.0) converts range to about
    # (-4.0, 4.0)

    threshold_matrix = 1.0 / (1.0 + np.exp(-((x - 128.0) / 32.0)))
    return threshold_matrix


def color_select(threshold_matrix, colors):

    # Takes a matrix of thresholds and returns a matrix of correpsonding colors
    # The returned datatype is a matrix of 3-element tuples

    indices_matrix = (threshold_matrix * len(colors)).astype(int)
    return np.array(colors)[indices_matrix]

col = Image.open("test/profile.png")

blur = (col.size[0] * col.size[1]) / (blur_px_per_mp * math.pow(10, 6))
col = col.filter(ImageFilter.GaussianBlur(blur))

gray = col.convert('L')
col = col.convert('RGB')

bw = np.asarray(gray).copy()

threshold_matrix = sigmoid(bw)
col = color_select(threshold_matrix, colors)

#col = map(tuple, col)
imfile = toimage(col, mode='RGB')
imfile.save("test/profile_color.png")
