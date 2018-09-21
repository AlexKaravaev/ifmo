import numpy as np
from preprocess import *


def correct_outliners(data):
    min, max = data.min(), data.max()
    data = data.flatten()
    mean = np.mean(data)
    for index, elem in np.ndenumerate(data):
        if elem >= max or elem <= min:
            data[index[0]] = mean
    return data

if __name__ == '__main__':
    vals = preprocess()
    plt.plot(vals.flatten(), vals.flatten(),'go', label = 'before lin.approx')
    plt.legend()
    plt.show()
    corrected = correct_outliners(vals)
    plt.plot(corrected, corrected,'ro',label = 'after lin.approx')
    plt.legend()
    plt.show()
    print("result is : {}".format(corrected))
