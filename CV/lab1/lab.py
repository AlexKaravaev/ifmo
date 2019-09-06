import cv2
import numpy as np
import matplotlib
from PIL import Image
from matplotlib import pyplot as plt
from skimage.util import random_noise
from skimage import img_as_ubyte, feature
from skimage.filters import roberts, sobel, prewitt, laplace, 
from scipy.signal import wiener
from scipy.ndimage import rank_filter as _rank_filter
from typing import Tuple

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

def wiener_filter(img: np.ndarray, mask_size: tuple) -> np.ndarray:
    """ Apply wiener filtering to image
    
    Arguments:
        img {np.ndarray} -- input image
        mask_size {tuple} -- convolution mask size
    
    Returns:
        np.ndarray -- fiktered image
    """
    data = np.array(img, dtype=np.float64)
    data = data.ravel()
    res  = wiener(data, mask_size[0])
    return res.reshape(img.shape).astype(np.uint8)

def rank_filter(img: np.ndarray, rank: int, mask_size: tuple) -> np.ndarray:
    """ Apply rank filtering to image
    
    Arguments:
        img {np.ndarray} -- input image
        rank {int} -- rank parameter
        mask_size{tuple} -- footprint size
    Returns:
        np.ndarray -- filtered image
    """
    data = np.array(img, dtype=np.float64)
    data = data.ravel()
    res  = _rank_filter(input=data, rank=rank, footprint=mask_size)
    return res.reshape(img.shape).astype(np.uint8)

def create_window(x: int, y: int, window: np.ndarray, 
                    img: np.ndarray) -> Tuple[np.ndarray, np.ndarray, int]:
    """ Creates window, sorts it and finds median
    
    Arguments:
        x {int} -- x start idx
        y {int} -- y start idx
        win {np.ndarray} -- window array
        img {np.ndarray} -- img array
    
    Returns:
        np.ndarray -- filled window
        np.ndarray -- target vector
        int        -- length of vector
    """
    ax = x
    ay = y

    W = 2 * window + 1
    vlength = W * W

    """Creating the window"""
    filter_window = np.array(np.zeros((W, W)))
    target_vector = np.array(np.zeros(vlength))

    img = np.pad(img, window, mode='constant')

    """populate window, sort, find median"""
    filter_window = img[ay:ay+(window*2)+1, ax:ax+(window*2)+1]
    target_vector = np.reshape(filter_window, ((vlength),))

    return filter_window, target_vector, vlength


def calc_median(target_array, array_length):
    sorted_array = np.sort(target_array)
    Zmed = sorted_array[int(array_length/2)]
    Zmin = sorted_array[0]
    Zmax = sorted_array[int(array_length-1)]
    return Zmin, Zmed, Zmax

def adaptive_median_filter(img: np.ndarray, mask_size: tuple, window: int, thresh: float) -> np.ndarray:
    # TODO for now naive implementation with pure python, can be optimized via numpy
    """ Apply adaptive median filter to image
    
    Arguments:
        img {np.ndarray} -- input image
        mask_size {tuple} -- mask size
        window {int} -- window size
        thresh {float} -- threshold value
    
    Returns:
        np.ndarray -- filtered image`
    """
    
    min_window, max_window = 1,4
    xlength, ylength = img.shape[0], img.shape[1]

    img_array = np.reshape(np.array(img), (ylength, xlength))

    pixel_count = 0    
    
    for y in range(0, ylength):
        for x in range(0, xlength):
            window = min_window
            while (window <= max_window):
                """Creating and populating window"""
                filter_window, target_vector, vlength = create_window(
                    x, y, window, img_array)

                """calculating the median for the window"""
                Zmin, Zmed, Zmax = calc_median(target_vector, vlength)
                A1 = int(Zmed) - int(Zmin)
                A2 = int(Zmed) - int(Zmax)
                if (A1 > 0 and A2 < 0):
                    B1 = int(img_array[y, x]) - int(Zmin)
                    B2 = int(img_array[y, x]) - int(Zmax)
                    if not(B1 > 0 and B2 < 0):
                        img_array[y, x] = Zmed
                        pixel_count += 1
                        break
                    else:
                        break
                else:
                    window += 1

    return np.reshape(img_array, (xlength*ylength,)).astype(np.uint8)

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

    # Median, weighted median, rang and Winner filtering
    cv2.imwrite(dir_ + 'median.jpg', cv2.medianBlur(gauss, 1))
    
    cv2.imwrite(dir_ + 'weighted_median.jpg', cv2.medianBlur(gauss, 3))
    
    cv2.imwrite(dir_ + 'wiener.jpg', wiener_filter(gauss, (3,3)))
   
    cv2.imwrite(dir_ + 'rank.jpg', rank_filter(gauss, -1, (3,3)))
    
    cv2.imwrite(dir_ + 'adaptive_median.jpg', adaptive_median_filter(gauss, (3,3), 5, 5))
    