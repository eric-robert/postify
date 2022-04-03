from re import X
from .. import Color, Cache, Border, Line, Text, Convert, Effects, To
import random
import numpy as np
import cv2, math, random

def Sparkles ( poster = None, count = 20, size = 40, cut = 50):

    # Get poster
    if poster is None:
        poster = Cache.get_last_img()
    
    count *= np.sum(poster) / 100_000_000
    count = int(count)

    size, _ = Convert.to_pixels(width = size / 1000)
    cut, _ = Convert.to_pixels(width = cut / 1000)

    # Select the count brightest pixels on the frame

    positions = []
    view = np.sum(poster,axis=(2)).astype(float)
    overlay = np.zeros((poster.shape)).astype(float)

    # Choose
    for i in range(count):

        brightest = np.argmax(view)

        y = brightest // poster.shape[1]
        x = brightest % poster.shape[1]

        if view[y,x] <= 0: break

        positions.append((x,y))
        if (y-cut < 0):
            cut = y
        if (x-cut < 0):
            cut = x
        view[y-cut:y+cut,x-cut:x+cut] -= 20
        view[y,x] = 0

    # Apply
    chose_size = []
    chose_color = []
    for x,y in positions:

        _size = random.randint(2, size * (1+random.randint(0,7)//6))
        r = random.randint(18,35)
        g = random.randint(18,35)
        b = random.randint(18,35)
        _color = (r,g,b)
        chose_size.append(_size)
        chose_color.append(_color)

        overlay[y-1:y+1,x-_size:x+_size] += (r,g,b)
        overlay[y-_size:y+_size,x-1:x+1] += (r,g,b)
        
    overlay[overlay>255] = 255
    overlay = cv2.blur(overlay, (50,50))
    overlay = cv2.blur(overlay, (50,50))
    overlay *= 128 / overlay.max()

    for i,p in enumerate(positions):

        x,y = p
        _size = chose_size[i]
        color = chose_color[i]

        overlay[y-1:y+1,x-_size:x+_size] += color
        overlay[y-_size:y+_size,x-1:x+1] += color


    overlay[overlay>255] = 255
    overlay = cv2.blur(overlay, (5,5))
    overlay *= 128 / overlay.max()

    poster = poster.astype(float)
    poster[:,:] += overlay
    poster[poster > 255] = 255
    Cache.set_last_img(poster)