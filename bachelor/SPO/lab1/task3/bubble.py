import math
from algo import *

class Bubble(Algo):

    def __init__(self, array_to_be_sorted):
        super().__init__(array_to_be_sorted)

    def sort(self):
        for pass_number in range(len(self.array)-1, 0, -1):
            for i in range(pass_number):
                if self.array[i]>self.array[i+1]:
                    self.array[i], self.array[i+1] = self.array[i+1], self.array[i]

if __name__ == '__main__':
    print("TESTING")
    array = [53,12,35,132,245,31,3]
    sort = Bubble(array)
    sort.sorted_with_time()
    sort.result()
