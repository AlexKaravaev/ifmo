import cv2
from closedcv.segmentation import *
from skimage.segmentation import slic
from skimage.color import xyz2lab
from skimage import img_as_ubyte
from skimage.segmentation import (morphological_chan_vese,
                                  morphological_geodesic_active_contour,
                                  checkerboard_level_set)

if __name__=="__main__":
    img = cv2.imread('./input/face.jpg', 1)

    dir_ = './res/'

    ret, thresh = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

    cv2.imwrite(dir_ + 'binarized.jpg', thresh)

    cv2.imwrite(dir_ + 'face.jpg', detect_face(img))

    # Convert to CIE-LAB+
    img = xyz2lab(cv2.imread('./input/balls.jpg', 1))
    #cv2.imwrite(dir_ + 'k_means.jpg', img_as_ubyte(slic(img, n_segments=117, max_iter=30, sigma=1, compactness=0.75,
    #        multichannel=True)))

    img = cv2.imread('./input/texture.jpeg', 0)
    
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imwrite(dir_ + 'texture_thresh.jpg', thresh)

    kernels = [np.ones((i*5, i*5), np.uint8) for i in range(6)]
    for kernel in kernels:
        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        cv2.imwrite(dir_ + 'texture_k' + str(kernel.shape) + '.jpg', closing)