
import cv2
import numpy as np
from PIL import Image
from skimage import img_as_ubyte
from skimage.morphology import black_tophat, disk, erosion

if __name__ == "__main__":

    dir_ = './res/'

    img = cv2.imread('./input/Open_box.jpg', 0)
    selem = disk(20)
    scikit_img = img_as_ubyte(img)
    removed_open = erosion(scikit_img, selem)
    cv2.imwrite(dir_ + 'removed_damage.jpg', removed_open)

    img = cv2.imread('./input/circles.jpg', 0)
    selem = disk(10)
    scikit_img = img_as_ubyte(img)
    removed_open = erosion(scikit_img, selem)
    cv2.imwrite(dir_ + 'removed_edges.jpg', removed_open)