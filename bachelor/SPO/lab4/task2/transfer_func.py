import random


def out (matrix):
    if matrix != None:
        for i in range (0, len(matrix)):
            print(matrix[i])
    return " "


def func(A, B, C):
    koef = []
    k1 = -A[0][0] * A[1][1] * A[2][2] + A[0][0] * A[2][1] * A[1][2] + A[1][0] * A[2][2] * A[0][1] - A[1][0] * A[0][2] * \
         A[2][1] - A[2][0] * A[0][1] * A[1][2] + A[0][2] * A[1][1] * A[2][0]
    koef.append(k1)
    k2 = A[1][1] * A[2][2] - A[2][1] * A[1][2] + A[0][0] * A[2][2] + A[0][0] * A[1][1] - A[1][0] * A[0][1] - A[2][0] * \
         A[0][2]
    koef.append(k2)
    k3 = -A[0][0] - A[1][1] - A[2][2]
    koef.append(k3)
    koef.append(1)
    koef2 = []
    k12 = ((A[0][0] * A[1][1]-A[0][1]*A[1][0])*B[2][0]+(-A[0][0]*A[2][1]+A[0][1]*A[2][0])*B[1][0]
           +(A[1][0]*A[2][1]-A[1][1]*A[2][0])*B[0][0])*C[0][2]+((-A[0][0]*A[1][2]+A[0][2]*A[1][0])*B[2][0]
            +(A[0][0]*A[2][2]-A[0][2]*A[2][0])*B[1][0]+(-A[1][0]*A[2][2]+A[1][2]*A[2][0])*B[0][0])*C[0][1]\
          +((A[0][1]*A[1][2]-A[0][2]*A[1][1])*B[2][0]+(-A[0][1]*A[2][2]+A[0][2]*A[2][1])*B[1][0]
            +(A[1][1]*A[2][2]-A[1][2]*A[2][1])*B[0][0])*C[0][0]
    koef2.append(k12)
    k22 = (((-A[1][1]-A[0][0])*B[2][0]+A[2][1]*B[1][0]+A[2][0]*B[0][0])*C[0][2]+(A[1][2]*B[2][0]
            +(-A[2][2]-A[0][0])*B[1][0]+A[1][0]*B[0][0])*C[0][1]
           +(A[0][2]*B[2][0]+A[0][1]*B[1][0]+(-A[2][2]-A[1][1])*B[0][0])*C[0][0])
    koef2.append(k22)
    k32 = ((B[0][0] * C[0][0]) + (B[1][0] * C[0][1]) + (B[2][0] * C[0][2]))
    koef2.append(k32)

    signs = []
    sign = "+" if koef2[0] > 0 else "-"
    signs.append(sign)
    sign = "+" if koef2[1] > 0 else "-"
    signs.append(sign)
    sign = "" if koef2[2] > 0 else "-"
    signs.append(sign)

    print(signs[2] + str(abs(koef2[2])) + 's^2' + signs[1] + str(abs(koef2[1])) + 's' + signs[0] + str(abs(koef2[0])))

    signs = []
    sign = "+" if koef[0] > 0 else "-"
    signs.append(sign)
    sign = "+" if koef[1] > 0 else "-"
    signs.append(sign)
    sign = "+" if koef[2] > 0 else "-"
    signs.append(sign)

    print("—"*16)
    print('s^3' + signs[0] + str(abs(koef[2])) + 's^2' + signs[1] + str(abs(koef[1])) + 's' + signs[0] + str(
        abs(koef[0])))
    print('\n')


if __name__ == "__main__":

    A = [[random.randint(-10, 10) for i in range(3)] for i in range(3)]
    B = [[random.randint(-10, 10)] for i in range(3)]
    C = [[random.randint(-10, 10) for i in range(3)]]

    print("Матрица А:")
    print(out(A))
    print('\n')
    print("Матрица B:")
    print(out(B))
    print('\n')
    print("Матрица C:")
    print(out(C))
    print('\n')
    print("Передаточная функция системы:")
    func(A, B, C)
