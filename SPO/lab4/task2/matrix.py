import copy
import random


class Matrix:
    def __init__(self, matrix):
        try:
            self.__rows = len(matrix)
            self.__cols = len(matrix[0])
        except IndexError:
            raise ValueError("A matrix cannot be empty")

        if not all([len(row) == self.__cols for row in matrix]):
            raise ValueError("All colums have to be of equal length")

        self.__matrix = matrix

    @classmethod
    def zero_matrix(self, rows, cols):
        matrix = [[0 for i in range(cols)] for j in range(rows)]
        return Matrix(matrix)

    def mul(self, rhs):
        result = Matrix.zero_matrix(self.rows(), rhs.cols())

        for i in range(self.rows()):
            for j in range(rhs.cols()):
                for k in range(self.cols()):
                    result[i, j] += int(self[i, k] * rhs[k, j])

        return result

    def min(self, rhs):
        result = Matrix.zero_matrix(self.rows(), rhs.cols())

        for i in range(self.rows()):
            for j in range(rhs.cols()):
                for k in range(self.cols()):
                    result[i, j] += int(self[i, k] - rhs[k, j])

        return result

    def determinant2(self, a, b, c, d):
        return a * d - b * c

    def get_matrix_minors(self):
        result = Matrix.zero_matrix(self.rows(), self.cols())

        result[0, 0] = self.determinant2(self[1, 1], self[1, 2], self[2, 1], self[2, 2])
        result[0, 1] = -self.determinant2(self[1, 0], self[1, 2], self[2, 0], self[2, 2])
        result[0, 2] = self.determinant2(self[1, 0], self[1, 1], self[2, 0], self[2, 1])

        result[1, 0] = -self.determinant2(self[0, 1], self[0, 2], self[2, 1], self[2, 2])
        result[1, 1] = self.determinant2(self[0, 0], self[0, 2], self[2, 0], self[2, 2])
        result[1, 2] = -self.determinant2(self[0, 0], self[0, 1], self[2, 0], self[2, 1])

        result[2, 0] = self.determinant2(self[0, 1], self[0, 2], self[1, 1], self[1, 2])
        result[2, 1] = -self.determinant2(self[0, 0], self[0, 2], self[1, 0], self[1, 2])
        result[2, 2] = self.determinant2(self[0, 0], self[0, 1], self[1, 0], self[1, 1])

        return result

    def transp(self):
        result = Matrix.zero_matrix(self.rows(), self.cols())

        for i in range(self.rows()):
            for j in range(self.cols()):
                result[i, j] = self[i, j]

        result[0, 1], result[1, 0] = self[1, 0], self[0, 1]
        result[0, 2], result[2, 0] = self[2, 0], self[0, 2]
        result[1, 2], result[2, 1] = self[2, 1], self[1, 2]

        return result

    def determinant3(self):
        return self[0, 0] * (self[1, 1] * self[2, 2] - self[1, 2] * self[2, 1]) - self[0, 1] * (self[1, 0] * self[2, 2] - self[1, 2] * self[2, 0]) + self[0, 2] * (self[1, 0] * self[2, 1] - self[1, 1] * self[2, 0])

    def inv(self):
        result = self.get_matrix_minors().transp()
        det = self.determinant3()

        for i in range(self.rows()):
            for j in range(self.cols()):
                result[i, j] = result[i, j] / det

        return result

    def rank(self):
        """calls gauss method"""

        gauss_matrix = self.gauss()
        result = self.rows()

        def is_zero_row(row):
            return all([elem == 0 for elem in row])

        for row in gauss_matrix:
            if is_zero_row(row):
                result -= 1

        return result

    def gauss(self):
        """triangularly shapes matrix"""

        x = copy.deepcopy(self)

        for i in range(min(self.rows(), self.cols())):
            for j in range(i + 1, self.rows()):
                c = x[j, i] / x[i, i] if x[i, i] != 0 else 0
                for k in range(self.cols()):
                    x[j, k] = int(x[j, k] - c * x[i, k])

        return x

    def rows(self):
        return self.__rows

    def cols(self):
        return self.__cols

    def __iter__(self):
        for row in self.__matrix:
            yield row

    def __setitem__(self, key, value):
        x, y = key
        self.__matrix[x][y] = value

    def __getitem__(self, key):
        x, y = key
        return self.__matrix[x][y]

    def __str__(self):
        return '[' + ',\n '.join([''.join(str(row)) for row in self.__matrix]) + ']'


def gen_matrix(r, c):
    rows = int(r)
    matrix = []
    for row in range(rows):
        x = [random.randint(0, 40) for i in range(c)]
        matrix += [x]
    return Matrix(matrix)

def gen_id_matrix(r, c):
    rows = int(r)
    matrix = []
    for row in range(rows):
        x = [0 for i in range(c)]
        x[row] = 1
        matrix += [x]
    return Matrix(matrix)
