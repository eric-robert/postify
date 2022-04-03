from .. import Color, Cache, Border, Line, Text, Convert, Effects
import random
import numpy as np
import cv2, math

def AproxBox ( poster = None, box_density = 0.005, background = (0,0,0), callback_count = 6, callback = None, high_detail = False):

    print("")
    
    # Get poster
    if poster is None:
        poster = Cache.get_last_img()
    
    # Get pixels for even borders
    total_pix = poster.shape[0] * poster.shape[1]
    lines = int(total_pix * box_density)
    callback_number = lines // (callback_count )

    # Create canvas
    new_poster = np.zeros((poster.shape[0], poster.shape[1], 3))
    new_poster[:,:] = background

    for i in range(lines):

        print("\rCreating AproxBox: {}%".format(round(i/lines*100, 2)), end="\r")

        if i % callback_number == 0:
            if i/lines < 0.9:
                if callback is not None:
                    Cache.set_last_img(new_poster)
                    callback()
                    new_poster = Cache.get_last_img()
                
        left = 1 - (i / lines)
        if (high_detail):
            left //= 2

        x = random.randint(0, poster.shape[1]-5)
        y = random.randint(0, poster.shape[0]-5)

        w = random.randint(1, 2+math.floor(left * (poster.shape[1] - x - 1)))
        h = random.randint(1, 2+math.floor(left * (poster.shape[0] - y - 1)))

        # Get avearge color
        patch_poster = poster[y:y+h, x:x+w]
        patch_aprox = new_poster[y:y+h, x:x+w]
        color = np.average(poster[y:y+h, x:x+w], axis=(0,1))

        # See if average is a better match
        score_current = np.sum(np.abs(patch_poster - patch_aprox))
        score_aprox = np.sum(np.abs(patch_poster - color))

        if score_aprox < score_current:
            new_poster[y:y+h, x:x+w] = color

    new_poster[new_poster < 0] = 0
    new_poster[new_poster > 255] = 255

    print("\rCreating AproxBox: 100%", ' ' * 10)

    Cache.set_last_img(new_poster)

