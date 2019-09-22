
import cv2
import numpy as np
from PIL import Image
from skimage import img_as_ubyte
from skimage.morphology import black_tophat,thin, disk, erosion, skeletonize, closing, watershed
from skimage.util import invert
from skimage.filters import threshold_minimum as binary, rank
from skimage.feature import peak_local_max
from skimage import io
from skimage.color import label2rgb
from scipy import ndimage as ndi

if __name__ == "__main__":

    dir_ = './res/'

    img = cv2.imread('./input/Open_box.jpg', 0)
    selem = disk(20)
    scikit_img = img_as_ubyte(img)
    removed_open = erosion(scikit_img, selem)
    cv2.imwrite(dir_ + 'removed_damage.jpg', removed_open)

    # img = cv2.imread('./input/circles.jpg', 0)
    # selem = disk(55)
    # thresh = binary(img_as_ubyte(img))
    # scikit_img = ~img_as_ubyte(img)
    # erosed = erosion(scikit_img, selem)
    # closed = closing(erosed, selem)
    # #removed_open = skeletonize(erosed).astype(np.uint8)
    # #print(removed_open)
    # cv2.imwrite(dir_ + 'removed_edges.jpg', closed)
    
    image =  img_as_ubyte(cv2.imread('./input/balls.jpg')) 
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = rank.median(image, disk(1))
    
    # find continuous region (low gradient -
    # where less than 10 for this image) --> markers
    # disk(5) is used here to get a more smooth image
    markers = rank.gradient(denoised, disk(10)) < 10
    markers = ndi.label(markers)[0]

    # local gradient (disk(2) is used to keep edges thin)
    gradient = rank.gradient(denoised, disk(1))
    cv2.imwrite(dir_ + 'gradient.jpg', gradient)
    
    # process the watershed
    labels = watershed(gradient, markers)



    cv2.imwrite(dir_ + 'watershed.jpg', labels)
