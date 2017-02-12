from PIL import Image, ImageFilter
import numpy as np
import math


def sigmoid(x):

    # result is between 0 and 1
    # since values between 0 and 255, (x-128)/32.0) converts range to about
    # (-4, 4)

    result = 1 / (1 + math.exp(-((x - 128) / 32.0)))

    if result < 0.25:
        return (26, 26, 26)
    elif result < 0.50:
        return (255, 255, 255)
    elif result < 0.75:
        return (189, 195, 199)
    else:
        return (44, 62, 80)

col = Image.open("profile.png").filter(ImageFilter.GaussianBlur(2))

gray = col.convert('L')
col = col.convert('RGB')

bw = np.asarray(gray).copy()
col = np.asarray(col).copy()

for index, x in np.ndenumerate(bw):
    col[index] = sigmoid(x)

imfile = Image.fromarray(col)
imfile = imfile.filter(ImageFilter.GaussianBlur(2))
imfile.save("profile_color.png")
