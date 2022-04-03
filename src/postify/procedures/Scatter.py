from .. import Color, Cache, Border, Line, Text, Convert, Effects
import random
import numpy as np
import cv2, math

def Scatter ( poster = None, min_size = 0, size = 32, scatter_density = 0.0005, decay_factor = 1.3, fade_factor = 0.8, background = (0,0,0)):

    print("")

    start_size = size
    
    # Get poster
    if poster is None:
        poster = Cache.get_last_img()
    
    # Create canvas
    new_poster = np.zeros((poster.shape[0], poster.shape[1], 3))
    new_poster[:,:] = background

    mesh = np.meshgrid(range(poster.shape[1]), range(poster.shape[0]))
    mesh = np.array(mesh)
    mesh = np.moveaxis(mesh, 0, -1)
    mesh = np.moveaxis(mesh, 0, 1)

    while True:

        size //= decay_factor
        size = int(size)
        print("\rCreating Scatter: {}%".format(round( 1 - (size/start_size), 2) * 100), end="\r")

        positions = np.random.rand(poster.shape[0] * poster.shape[1])
        positions = np.reshape(positions, (poster.shape[0], poster.shape[1]))
        positions = np.where(positions < scatter_density)
        positions = np.array(positions).T

        for dx in range(-size, size):
            for dy in range(-size, size):
                _pos = positions + (dx, dy)
                _pos[_pos > (poster.shape[0]-1)] = poster.shape[0]-1
                _pos[_pos < 0] = 0
                _pos[_pos>=poster.shape[1]] = poster.shape[1]-1
                new_poster[_pos[:,0], _pos[:,1]] = poster[positions[:,0], positions[:,1]]

        new_poster[positions[:,0], positions[:,1]] = poster[positions[:,0], positions[:,1]]
        new_poster *= fade_factor

        if size <= min_size:
            break

    
    print("\rCreating Scatter: 100%", end="\r")

    Cache.set_last_img(new_poster)

