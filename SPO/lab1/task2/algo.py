import timeit

class Algo:

    def __init__(self, array_to_be_sorted):
        self.array = array_to_be_sorted

    def result(self):
        print("Sorted array {} \nwith execution time: {}".format(self.array, self.exec_time))

    def sorted_with_time(self):
        start_time = timeit.default_timer()
        self.sort()
        self.exec_time = timeit.default_timer() - start_time
        
