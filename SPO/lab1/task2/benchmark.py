from bubble import *
from bucket import *
from gnome import *
from heapsort import *
import numpy.random as nprnd

if __name__ == '__main__':

    sorts = [Gnome([]), Bucket([]), Heapsort([]), Bubble([])]
    times = [0 for i in range(4)]

    n = 500

    for i in range(n):
        rand_arr = nprnd.randint(1000, size = 100)

        for i, sort in enumerate(sorts):
            sort.change_arr(rand_arr)
            sort.sorted_with_time()
            times[i] += sort.get_time()

    print("These are average times of each sort")
    for i, sort in enumerate(sorts):
        ans = sort.__class__.__name__ + ": " + str(times[i]/n)
        print(ans)
