import numpy as np
from preprocess import *
import random
import copy
import sys
import math

def lin_correlation(x,y):
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    cov = 0
    s_x = 0
    s_y = 0
    for i in range(x.shape[0]):
        cov += (x[i] - x_mean)*(y[i] - y_mean)
        s_x += (x[i] - x_mean)**2
        s_y += (y[i] - y_mean)**2
    r = cov/math.sqrt(s_x*s_y)
    return r

def exp_correlation(x,y):
    return lin_correlation(x, np.log(y))

def check_correlation(data):
    lin_corr_matrix = np.zeros((24,24))
    exp_corr_matrix = np.zeros((24,24))

    for i in range(24):
        for j in range(24):
            lin_corr_matrix[i][j] = lin_correlation(data[:,i],data[:,j])
            exp_corr_matrix[i][j] = exp_correlation(data[:,i],data[:,j])

    return lin_corr_matrix, exp_corr_matrix
if __name__ == '__main__':
    vals = preprocess()
    ans = check_correlation(vals)

    print("Лин.зависимость")
    print(np.dstack(np.where(abs(ans[0]) > 0.7)))
    print("Эксп.зависимость")
    print(np.dstack(np.where(abs(ans[1]) > 0.7)))
