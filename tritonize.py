from PIL import Image, ImageFilter
import numpy as np
import math

colors = [(26, 26, 26), (255, 255, 255), (44, 62, 80)]
blur_px_per_mp = 1


def sigmoid(x):

    # result is between 0 and 1
    # since values between 0 and 255, (x-128)/32.0) converts range to about
    # (-4.0, 4.0)

    return 1 / (1 + math.exp(-((x - 128) / 32.0)))

col = Image.open("test/profile.png")

blur = (col.size[0] * col.size[1]) / (blur_px_per_mp * math.pow(10, 6))
col = col.filter(ImageFilter.GaussianBlur(blur))

gray = col.convert('L')
col = col.convert('RGB')

bw = np.asarray(gray).copy()
col = np.asarray(col).copy()

for index, x in np.ndenumerate(bw):
    threshold = sigmoid(x)
    col[index] = colors[int(math.floor(threshold * len(colors)))]

imfile = Image.fromarray(col)
imfile.save("test/profile_color.png")
