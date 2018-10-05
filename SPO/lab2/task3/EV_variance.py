import numpy as np
from preprocess import *
import random
import copy
import sys

def expected_value(data):
    ev_list = []
    for col in data.T:
        unique, counts = np.unique(col, return_counts = True)
        freq = dict(zip(unique, counts))
        ev = sum([(x*(freq.get(x)/col.shape[0])) for x in freq.keys()])
        ev_list.append(ev)
    return ev_list

def variance(data, ev, ev_sqr):
    var_list = []
    index = 0
    for col in data.T:
        var = ev_sqr[index] - ev[index]**2
        var_list.append(var)
        index += 1
    return var_list

if __name__ == '__main__':
    vals = preprocess()
    ev = expected_value(vals)
    ev_sqr = expected_value(np.square(vals))

    variance = variance(vals, ev, ev_sqr)
    print("Мат.ожидание: {}".format(ev))
    print("Дисперсия: {}".format(variance))
    for i in variance:
        sys.stdout.write("{0:.3f} & ".format(i))
