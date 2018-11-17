from matrix import *

if __name__ == "__main__":
    A = gen_matrix(3, 3)
    B = gen_matrix(3, 1)
    C = gen_matrix(1, 3)
    I = gen_id_matrix(3, 3)
    print(I.min(A))
