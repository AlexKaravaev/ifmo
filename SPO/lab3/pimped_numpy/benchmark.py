from lib.pimped_numpy import *
import random
import numpy
import timeit

if __name__ == "__main__":
    times = [0 for _ in range(2)]
    n = 100
    for _ in range(100):
        
        matrix = [[random.randint(-100,100) for i in range(100)] for i in range(100)]
        np_matrix = numpy.random.randint(low = -100,high = 100, size = (100,100))
        
        s_time = timeit.default_timer()
        rank(matrix)
        exec_time = timeit.default_timer() - s_time
        times[0] += exec_time

        s_time = timeit.default_timer()
        numpy.linalg.matrix_rank(np_matrix)
        exec_time = timeit.default_timer() - s_time
        times[1] += exec_time

    times = [elem/n for elem in times]
    print("Mean time for my algo: {}\n Mean time for np algo: {}\n".format(times[0],times[1]))
