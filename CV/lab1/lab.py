import cv2
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from skimage.util import random_noise
matplotlib.rcParams["backend"] = "TkAgg"

def contraharmonic_filter(img: np.ndarray, Q: int, mask_size: tuple) -> np.ndarray:
    """ Apply contraharmonic filter to input image
    
    Arguments:
        img {np.ndarray} -- image
        Q {int} -- Q paramater
        mask_size {tuple} -- convolution mask size
    
    Returns:
        np.ndarray -- filtered image
    """
    h, w = img.shape[0], img.shape[1]
    filtered = np.zeros(shape = img.shape)
    for row in range(mask_size[0]//2 , h - mask_size[0]//2 - 1):
        for col in range(mask_size[1] // 2, w - mask_size[1]//2 - 1):
            kernel = np.array([img[row + i][col + j] for j in range(-mask_size[0]//2, (mask_size[0] // 2) + 1)
                            for i in range(-mask_size[1] // 2, (mask_size[1] // 2) + 1)])
            num   = np.sum(kernel ** (Q + 1))
            denum = np.sum(kernel ** Q)
            filtered[row][col] = num / denum
    return filtered
    
if __name__=="__main__":
    img = cv2.imread('../img.jpeg', 0); 
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gauss = random_noise(img, mode='gaussian', seed=None, clip=True)

    cntrharmonic = contraharmonic_filter(img, 1,(3,3))
    cv2.imshow('original', img)
    cv2.imshow('contraharmonic_filter', cntrharmonic)
    cv2.waitKey()