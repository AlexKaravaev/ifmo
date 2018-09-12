import math
from algo import *

class Gnome(Algo):

    def __init__(self, array_to_be_sorted):
        super().__init__(array_to_be_sorted)

    def sort(self):
        i = 0
        while i < len(self.array):
            if i == 0 or self.array[i-1] <= self.array[i]:
                i+=1
            else:
                self.array[i], self.array[i-1] = self.array[i-1],self.array[i]
                i -= 1




if __name__ == '__main__':
    print("TESTING")
    array = [53,12,35,132,245,31,3]
    sort = Gnome(array)
    sort.sorted_with_time()
    sort.result()
