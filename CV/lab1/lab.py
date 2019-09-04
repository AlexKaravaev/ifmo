import cv2
import numpy as np
import matplotlib
from PIL import Image
from matplotlib import pyplot as plt
from skimage.util import random_noise
from skimage import img_as_ubyte
matplotlib.rcParams["backend"] = "TkAgg"
np.set_printoptions(threshold=np.inf)

def filter(img: np.ndarray, filter: np.ndarray) -> np.ndarray:
    """ Generic function, that applies filter-mask to each pixel of image
    
    Arguments:
        img {np.ndarray} -- input image
        filter {np.ndarray} -- filter array
    
    Returns:
        np.ndarray -- filtered image
    """
    h = w = img.shape[0]
    f_h, f_w = filter.shape[0], filter.shape[1]

    flat_filter = filter.ravel()
    return np.correlate(img, flat_filter, 'same')

def contraharmonic_filter(img: np.ndarray, Q: int, mask_size: tuple) -> np.ndarray:
    """ Apply contraharmonic filter to input image
    
    Arguments:
        img {np.ndarray} -- image
        Q {int} -- Q paramater
        mask_size {tuple} -- convolution mask size
    
    Returns:
        np.ndarray -- filtered image
    """
    
    data = np.array(img, dtype=np.float64)
    data = data.ravel()
    num = np.power(data, Q + 1)
    den = np.power(data, Q)
    kernel = np.full(mask_size, 1.0)

    res = filter(num, kernel)/filter(den,kernel)
    return res.reshape(img.shape).astype(np.uint8)

if __name__=="__main__":
    img = cv2.imread('../img.jpeg', 0)
    
    # Apply noise to input image
    gauss = random_noise(img, mode='gaussian', seed=None, clip=True)
    gauss = img_as_ubyte(gauss)
    dir_  = './res/'
    cv2.imwrite(dir_ + 'gauss.jpeg', gauss)

    Q = [-1, 0, 1]
    for q in Q:
        cntrharmonic = contraharmonic_filter(gauss, q,(3,3))
        cv2.imwrite(dir_ + 'contraharmonic_Q_' + str(q) + '.jpg', cntrharmonic)
    
    for q in Q:
        gauss_blur = cv2.GaussianBlur(gauss, (3,3), q)
        cv2.imwrite(dir_ + 'gaussian_Q_' + str(q) + '.jpg', gauss_blur)

