from skimage import data, exposure
from skimage.util import img_as_ubyte, img_as_float
import matplotlib.pyplot as plt
import numpy as np


def convertToUint(array):
    array[array > 255] = 255
    array[array < 0] = 0
    return array.astype('uint8')

def toGraph(array, row):
    for i in range(array.shape[2]):
        hist, hist_centers = exposure.histogram(array[..., i])
        axs[row, 1].plot(hist_centers, hist)


# original image
im = data.chelsea()


#--------------Арифметические операции----------------------
im_arithm = data.chelsea().astype('float')
to_add = 50
im_arithm += to_add
im_arithm = convertToUint(im_arithm)


#--------------Нелинейное растяжение динамического диапазона-----------
im_nonLinear = img_as_float(data.chelsea())
nonLinear_alpha = 0.5
for i in range(im_nonLinear.shape[2]):
    min = im_nonLinear[:,:,i].min()
    max = im_nonLinear[:,:,i].max()
    im_nonLinear[:,:,i] = ((im_nonLinear[:,:,i] - min) / (max - min)) ** nonLinear_alpha
im_nonLinear = img_as_ubyte(im_nonLinear)

#--------------Равномерное преобразование-----------------------------
im_uniformly = img_as_float(data.chelsea())
im_uniformly_index = data.chelsea()
for k in range(im_uniformly.shape[2]):
    min = im_uniformly[:, :, k].min()
    max = im_uniformly[:, :, k].max()
    hist, hist_centers = exposure.histogram(im_uniformly[..., k])
    cs = np.cumsum(hist) / (im_uniformly.shape[0] * im_uniformly.shape[1])
    for i in range(im_uniformly.shape[0]):
        for j in range(im_uniformly.shape[1]):
            index = im_uniformly_index[i,j,k]
            im_uniformly[i,j,k] = ((max - min) * cs[index] + min)
im_uniformly = img_as_ubyte(im_uniformly)

#--------------Экспоненциальное преобразование-----------
im_exponent = img_as_float(data.chelsea())
im_exponent_index = data.chelsea()
exponent_alpha = 1
for k in range(im_exponent.shape[2]):
    min = im_exponent[:, :, k].min()
    hist, hist_centers = exposure.histogram(im_exponent[..., k])
    cs = np.cumsum(hist) / (im_exponent.shape[0] * im_exponent.shape[1])
    for i in range(im_exponent.shape[0]):
        for j in range(im_exponent.shape[1]):
            im_exponent[i,j,k] = min - (1 / exponent_alpha) * np.log10(1 - cs[im_exponent_index[i,j,k]])
im_exponent[im_exponent > 1.0] = 0.0
im_exponent = img_as_ubyte(im_exponent)


#--------------Преобразование по закону Рэлея-----------
im_rayleigh = img_as_float(data.chelsea())
im_rayleigh_index = data.chelsea()
rayleigh_alpha = 1
for k in range(im_rayleigh.shape[2]):
    min = im_rayleigh[:, :, k].min()
    hist, hist_centers = exposure.histogram(im_rayleigh[..., k])
    cs = np.cumsum(hist) / (im_rayleigh.shape[0] * im_rayleigh.shape[1])
    for i in range(im_rayleigh.shape[0]):
        for j in range(im_rayleigh.shape[1]):
            im_rayleigh[i,j,k] = min + np.sqrt(2 * rayleigh_alpha ** 2 * np.log10((1 / (1 - cs[im_rayleigh_index[i,j,k]])))) ** (1/2)


#--------------Преобразование по закону степени 2/3-----------
im_twoThree = img_as_float(data.chelsea())
im_twoThree_index = data.chelsea()
for k in range(im_twoThree.shape[2]):
    hist, hist_centers = exposure.histogram(im_twoThree[..., k])
    cs = np.cumsum(hist) / (im_twoThree.shape[0] * im_twoThree.shape[1])
    for i in range(im_twoThree.shape[0]):
        for j in range(im_twoThree.shape[1]):
            im_twoThree[i,j,k] = cs[im_twoThree_index[i,j,k]] ** 2/3


#--------------Гиперболическое преобразование---------------------
im_hyperbolic = img_as_float(data.chelsea())
im_hyperbolic_index = data.chelsea()
for k in range(im_hyperbolic.shape[2]):
    min = im_hyperbolic[:, :, k].min()
    hist, hist_centers = exposure.histogram(im_hyperbolic[..., k])
    cs = np.cumsum(hist) / (im_hyperbolic.shape[0] * im_hyperbolic.shape[1])
    for i in range(im_hyperbolic.shape[0]):
        for j in range(im_hyperbolic.shape[1]):
            im_hyperbolic[i,j,k] = min ** cs[im_hyperbolic_index[i,j,k]]


#--------------Графики--------------------------------------
fig, axs = plt.subplots(8, 2, figsize=(15,15))

axs[0, 0].set_title('Original Image')
axs[0, 0].imshow(im)
axs[0, 1].set_title('Histograms')
toGraph(im, 0)

axs[1, 0].set_title('Arithmetic')
axs[1, 0].imshow(im_arithm)
toGraph(im_arithm, 1)

axs[2, 0].set_title('Non-linear')
axs[2, 0].imshow(im_nonLinear)
toGraph(im_nonLinear, 2)

axs[3, 0].set_title('Uniform')
axs[3, 0].imshow(im_uniformly)
toGraph(im_uniformly, 3)

axs[4, 0].set_title('Exponential')
axs[4, 0].imshow(im_exponent)
toGraph(im_exponent, 4)

axs[5, 0].set_title('Rayleigh')
axs[5, 0].imshow(im_rayleigh)
toGraph(im_rayleigh, 5)

axs[6, 0].set_title('2/3')
axs[6, 0].imshow(im_twoThree)
toGraph(im_twoThree, 6)

axs[7, 0].set_title('Hyperbolic')
axs[7, 0].imshow(im_hyperbolic)
toGraph(im_hyperbolic, 7)

fig.tight_layout()

plt.show()
