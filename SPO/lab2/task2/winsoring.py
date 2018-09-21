import numpy as np
from preprocess import *


def winsore(data):
    min, max = data.min(), data.max()
    data = data.flatten()
    for index, elem in np.ndenumerate(data):
        if elem >= max or elem <= min:
            data[index[0]] = data[index[0]+1] if index[0] != len(data) - 1 else data[index[0] - 1]
    return data

if __name__ == '__main__':
    vals = preprocess()
    plt.plot(vals.flatten(), vals.flatten(),'go', label = 'before winsoring')
    plt.legend()
    plt.show()
    corrected = winsore(vals)
    plt.plot(corrected, corrected,'ro',label = 'after winsoring')
    plt.legend()
    plt.show()
    print("result is : {}".format(corrected))
