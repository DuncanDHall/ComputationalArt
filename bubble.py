import numpy as np


def distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def paint_bubble(im, center=None, radius=None):

    im.size

    if center == None:
        x_offset = np.random.randint(0, im.size[0])
        y_offset = np.random.randint(0, im.size[1])
    else:
        x_offset, y_offset = center
    if radius == None:
        radius = im.size[0] / 8


    # gather all pixels in circle
    circle = []
    y = 0
    for x in range(-int(radius), 0):
        while distance(x, y, 0, 0) <= radius:
            row = [(x0, y) for x0 in range(x, -x + 1)]
            for x0 in range(x, 1):
                circle.append((x0, y))
                circle.append((-x0, y))
                circle.append((x0, -y))
                circle.append((-x0, -y))
            y += 1

    # paint pixels
    pixels = im.load()
    for x0, y0 in circle:
        x = x0 + x_offset
        y = y0 + y_offset
        if x > 0 and x < im.size[0] and y > 0 and y < im.size[1]:
            pixels[x, y] = (0, 0, 0)

    return im
