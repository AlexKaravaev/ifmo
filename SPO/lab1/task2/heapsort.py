import math
from algo import *

def heapify(arr, n, i):
    largest = i
    child_l = 2 * i + 1
    child_r = child_l + 1

    # walk down the tree(list) and check if childs are less than root
    if child_l < n and arr[i] < arr[child_l]:
        largest = child_l

    if child_r < n and arr[largest] < arr[child_r]:
        largest = child_r
    # change the root, if it is smaller
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]

        heapify(arr, n, largest)

class Heapsort(Algo):

    def __init__(self, array_to_be_sorted):
        super().__init__(array_to_be_sorted)

    def sort(self):
        for i in range(len(self.array), -1, -1):
            heapify(self.array, len(self.array), i)

        for i in range(len(self.array)-1, 0, -1):
            self.array[i], self.array[0] = self.array[0], self.array[i]
            heapify(self.array, i, 0)





if __name__ == '__main__':
    print("TESTING")
    array = [53,12,35,132,245,31,3]
    sort = Heapsort(array)
    sort.sorted_with_time()
    sort.result()
