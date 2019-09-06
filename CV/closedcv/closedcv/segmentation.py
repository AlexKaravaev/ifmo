import cv2
import numpy as np

def detect_face(img:np.ndarray, bounds: tuple=None) -> np.ndarray:
    """ Detect face based on skin color
    
    Arguments:
        img {np.ndarray} -- Source image
    
    Keyword Arguments:
        bounds {tuple} -- Lower and upper bounds for skin color (default: {None})
    
    Returns:
        np.ndarray -- Mask with only face 
    """
    if not bounds:
        bounds = []
        bounds.append(np.array([0, 60, 80], dtype = "uint8"))
        bounds.append(np.array([20, 255, 255], dtype = "uint8"))

    converted = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    skinMask = cv2.inRange(converted, bounds[0], bounds[1])
 
    # apply a series of erosions and dilations to the mask
    # using an elliptical kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    skinMask = cv2.erode(skinMask, kernel, iterations = 2)
    skinMask = cv2.dilate(skinMask, kernel, iterations = 2)
 
    # blur the mask to help remove noise, then apply the
    # mask to the frame
    skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
    skin = cv2.bitwise_and(img, img, mask = skinMask)

    return skin

def 