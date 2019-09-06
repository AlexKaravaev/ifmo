import cv2
import numpy as np
import matplotlib
from PIL import Image
from matplotlib import pyplot as plt
from skimage.util import random_noise
from skimage import img_as_ubyte
from skimage.filters import roberts, sobel, prewitt, laplace
from closedcv.filters import *

matplotlib.rcParams["backend"] = "TkAgg"
np.set_printoptions(threshold=np.inf)


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
    
    #cv2.imwrite(dir_ + 'adaptive_median.jpg', adaptive_median_filter(gauss, (3,3), 5, 5))
    
    # Edge detectors 
    #roberts_ = img_as_ubyte(roberts(img))
    cv2.imwrite(dir_ + 'roberts.jpg', img_as_ubyte(roberts(img)))
    cv2.imwrite(dir_ + 'sobel.jpg', img_as_ubyte(sobel(img)))
    cv2.imwrite(dir_ + 'prewitt.jpg', img_as_ubyte(prewitt(img)))
    cv2.imwrite(dir_ + 'laplace.jpg', img_as_ubyte(laplace(img)))
    cv2.imwrite(dir_ + 'canny.jpg', cv2.Canny(img, 100, 200))
