from PIL import Image, ImageFilter
import numpy as np
import math

colors = [(26, 26, 26), (255, 255, 255), (44, 62, 80)]
blur_factor = 400*400/200000


def sigmoid(x):

    # result is between 0 and 1
    # since values between 0 and 255, (x-128)/32.0) converts range to about
    # (-4, 4)

    return 1 / (1 + math.exp(-((x - 128) / 32.0)))

col = Image.open("test/profile.png")
col = col.filter(ImageFilter.GaussianBlur(blur_factor))

gray = col.convert('L')
col = col.convert('RGB')

bw = np.asarray(gray).copy()
col = np.asarray(col).copy()

for index, x in np.ndenumerate(bw):
    threshold = sigmoid(x)
    col[index] = colors[int(math.floor(threshold * len(colors)))]

imfile = Image.fromarray(col)
imfile = imfile.filter(ImageFilter.GaussianBlur(blur_factor))
imfile.save("test/profile_color.png")
