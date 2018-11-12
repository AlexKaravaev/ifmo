import numpy as np
import matplotlib.pyplot as plt
time = np.array([i for i in range(50)])

# test

def moving_average(input_list, n):
    plt.plot(time, input_list, 'ro-')
    filtered = [sum(input_list[i-n:i+n])/(2*n-1) for i in range(n,input_list.shape[0]-n)]
    print(filtered)
    plt.plot(time[n:len(filtered)+n], filtered, 'go-')
    plt.show()

def yesterday_as_tommorow(input_list):
    plt.plot(time, input_list, 'ro-')
    filtered = [input_list[i-1] for i in range(1,input_list.shape[0] - 1)]
    plt.plot(time[1:len(filtered)+1], filtered, 'go-')
    plt.show()

def weighted_average(input_list, weights):
    plt.plot(time, input_list, 'ro-')
    w_size = len(weights)
    filtered = np.zeros(shape = (len(input_list)))
    for i in range(w_size, input_list.shape[0]):
        temp_sum = 0
        for k in range(w_size):
            temp_sum += weights[k] * input_list[i-k]
        filtered[i] = temp_sum / w_size
    plt.plot(time[w_size:len(filtered)-w_size], filtered[w_size:-w_size], 'go-')
    plt.show()

def simple_exp(input_list, alpha):
    plt.plot(time, input_list, 'ro-')
    filtered = np.zeros(shape = input_list.shape)
    filtered[0] = input_list[0]
    for i in range(1,input_list.shape[0]):
        filtered[i] = alpha*input_list[i] + (1-alpha)*filtered[i-1]
    plt.plot(time, filtered, 'go-')
    plt.show()

if __name__ == "__main__":
    random_list = np.random.randint(low = 0, high = 40, size = (50))
    print(random_list)
    moving_average(random_list, 2)
    yesterday_as_tommorow(random_list)
    weighted_average(random_list, [0.9,0.8,0.75,0.6])
    simple_exp(random_list, 0.45)
