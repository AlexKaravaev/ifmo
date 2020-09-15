import numpy as np
from preprocess import *
import random

def parse_cols():
    input_str = input('Введите номера коррелирующих между собой столбцов в данном формате - 1,2;3,4,5;6,8): ')
    cols = [[int(i) for i in x.split(',')] for x in input_str.split(';')]
    return cols

def find_corr_col(cols, n_col):
    for col in cols:
        for elem in col:
            if n_col == elem:
                temp = col
                temp.pop(temp.index(n_col))
                return temp if isinstance(temp,int) else random.choice(temp)

def correct_outliners(data, corr_cols):
    n_col = 1
    for col in data.T:
        for index, elem in np.ndenumerate(col):
            if elem == -100:
                corr_col = find_corr_col(corr_cols, n_col)
                col[index[0]] = data[index[0]][corr_col - 1]/(data[index[0]-1][n_col]*data[index[0]-1][corr_col - 1])

        n_col += 1
    return data

if __name__ == '__main__':
    vals = preprocess()
    print('Номера столбцов, в которых отсутсвует значения')
    n_col = 1
    for col in vals.T:
        for index, elem in np.ndenumerate(col):
            if elem == -100:
                print(n_col)
        n_col += 1
    cols = parse_cols()
    plt.plot(vals.flatten(), vals.flatten(),'go', label = 'before lin.approx')
    plt.legend()
    plt.show()
    corrected = correct_outliners(vals, cols)
    plt.plot(corrected.flatten(), corrected.flatten(),'ro',label = 'after lin.approx')
    plt.legend()
    plt.show()
    print("result is : {}".format(corrected))
