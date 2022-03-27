import cv2
from . import Cache, Convert

def blur (poster = None, size = 0.02):

    # Get poster
    if poster is None:
        poster = Cache.get_last_img()
    
    # Get pixels for even borders
    size, _ = Convert.to_pixels(width=size, height=size)

    Cache.set_last_img(cv2.blur(poster, (size,size)))

def denoise (poster = None):

    if poster is None:
        poster = Cache.get_last_img()

    Cache.set_last_img(
        cv2.fastNlMeansDenoisingColored(poster,None,10,10,7,21)   
    )