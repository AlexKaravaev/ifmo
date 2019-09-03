import cv2
import numpy 
from matplotlib import pyplot as plt
from skimage.util import random_noise

if __name__=="__main__":
    img = cv2.imread('../img.jpeg', 0); 
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gauss = random_noise(img, mode='gaussian', seed=None, clip=True)

    # Gauss filtering and counter harmonic mean fiter
    plt.subplot(221), plt.imshow(img), plt.title('Origin')
    plt.subplot(222), plt.imshow(gauss), plt.title('Gaussian')
    plt.show();