import numpy as np

def contr_check(A, control):
    r_contr = rank(control)
    if size_m(A) == r_contr:
        print("Система управляема (ранг матрицы управляемости ", r_contr, ")")
    else:
        print("система не управляема, ранг матрицы управляемости ", r_contr)

def obs_check(A, obs):
    r_obs = rank(obs)
    if size_m(A) == r_obs:
        print("Система наблюдаема (Ранг матрицы наблюдаемости равен", r_obs, ")")
    else:
        print("Система не наблюдаема, ранг равен матрицы наблюдаемости равен ", r_obs)

def size_n(matrix):
    n = len(matrix[0])
    return n


def size_m(matrix):
    m = len(matrix)
    return m

def rank(matrix, n=0):
    """ Функции check (проверяет наличие нулевых строк и столбцов в матрице и удаляет их)
     и swap (если элемент a[i][i] равен 0, ищет в столбце ненулевой элемент и меняет строки так, чтобы a[i][i] != 0"""

    def check(matrix):
        list = []
        for i in range(0, size_m(matrix)):
            flag = 0
            for j in range(0, size_n(matrix)):
                if matrix[i][j] != 0: flag = 1
            if flag == 0:
                list.append(i)
        step = 0
        for i in list:
            del matrix[i - step]
            step += 1
        list = []
        for j in range(0, size_n(matrix)):
            flag = 0
            for i in range(0, size_m(matrix)):
                if matrix[i][j] != 0: flag = 1
            if flag == 0:
                list.append(j)
        step = 0
        for j in list:
            for i in range(0, size_m(matrix)):
                del matrix[i][j-step]
            step += 1
        return matrix

    def swap(matrix, i):
        k = 0
        if i == size_n(matrix) or i == size_m(matrix):
            pass
        else:
            for step in range(0, size_n(matrix) - i-1):
                if matrix[i][i] == 0:
                    matrix[i], matrix[i + step] = matrix[i + step], matrix[i]
                else:
                    k = 1
        return matrix, k

    ch_matr = check(matrix)
    f_matr, k = swap(ch_matr, n)
    minim = size_m(f_matr) if (size_m(f_matr)) <= size_n(f_matr) else size_n(f_matr)
    global r
    r = size_m(matrix)
    if (n < minim) or k != 0:
        for i in range(n + 1, size_m(f_matr)):
            koef = -f_matr[i][n] / f_matr[n][n]
            for j in range(n, size_n(f_matr)):
                f_matr[i][j] = koef * f_matr[n][j] + f_matr[i][j]  #
        rank(f_matr, n + 1)
    return r

if __name__ == '__main__':
	matrix = [[1,2,3,4],[1,2,3,4]]
	np_matrix = np.array(matrix)
	print(rank(matrix))
	print(np.linalg.matrix_rank(np_matrix))
	print(obs_check(matrix, matrix))
