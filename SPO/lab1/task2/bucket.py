import math
from algo import *

# helper function to sort buckets
def insertion_sort(array):
    if len(array) <= 1: return array
    i = 1
    while i < len(array):
        k = array[i]
        j = i - 1
        while j >= 0 and array[j] > k:
            array[j+1] = array[j]
            array[j] = k
            j -= 1
        i += 1
    return array

class Bucket(Algo):

    def __init__(self, array_to_be_sorted):
        super().__init__(array_to_be_sorted)

    def sort(self, bucketSize = 10):
        if len(self.array) == 0:
            return None

        minVal = self.array[0]
        maxVal = self.array[0]

        for _, elem in enumerate(self.array):
            if elem < minVal:
                minVal = elem
            elif elem > maxVal:
                maxVal = elem

        bucketCounter = math.floor((maxVal - minVal) / bucketSize) + 1
        buckets = [[] for i in range(bucketCounter)]


        for _, elem in enumerate(self.array):
            buckets[abs(math.floor((elem - minVal) / bucketSize))].append(elem)

        self.array = []
        for _, bucket in enumerate(buckets):
            sorted_bucket = insertion_sort(bucket)
            for _, item in enumerate(bucket):
                self.array.append(item)






if __name__ == '__main__':
    print("TESTING")
    array = [53,12,35,132,245,31,3]
    sort = Bucket(array)
    sort.sorted_with_time()
    sort.result()
