import math

def A(a, b):
    return b / (math.sqrt(a**2 + 5**2))

def A_out(a, b):
    return A(a, b) * 8

if __name__ == "__main__":
    a = int(input("a = "))
    b = int(input("b = "))
    print(A_out(a, b))
