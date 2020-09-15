# Вывод матрицы
def out(matrix):
	if matrix:
		for i in range (0, rows(matrix)):
			print(matrix[i])
	return " "

def rows(matrix):
	return len(matrix)


# Проверка устойчивости по Гурвицу
def gur(A):
	koef = []
	k1 = -A[0][0]*A[1][1]*A[2][2]+A[0][0]*A[2][1]*A[1][2]+A[1][0]*A[2][2]*A[0][1]-A[1][0]*A[0][2]*A[2][1]-A[2][0]*A[0][1]*A[1][2]+A[0][2]*A[1][1]*A[2][0]
	koef.append(k1)
	k2 = A[1][1]*A[2][2]-A[2][1]*A[1][2]+A[0][0]*A[2][2]+A[0][0]*A[1][1]-A[1][0]*A[0][1]-A[2][0]*A[0][2]
	koef.append(k2)
	k3 = -A[0][0]-A[1][1]-A[2][2]
	koef.append(k3)
	koef.append(1)
	print ("Характеристический полином:")
	print (str(koef[3])+'s^3+' + str(koef[2])+'s^2+'+str(koef[1])+'s+'+str(koef[0])+'=0')
	print('\n')
	matrix = [[koef[2],koef[0],0],[koef[3],koef[1],0],[0,koef[2],koef[0]]]
	print ("Матрица Гурвица:")
	print (out(matrix))
	if (koef[2] > 0) and (koef[1]*koef[2]-koef[0]*koef[3] > 0) and (koef[0]>0):
		return "Система устойчива (по Гурвицу)"
	if (koef[2] > 0) and (koef[1]*koef[2]-koef[0]*koef[3] > 0) and (koef[0]==0):
		return "Система на апериодической гнанице устойчивости (по Гурвицу)"
	if (koef[2] > 0) and (koef[1]*koef[2]-koef[0]*koef[3] == 0) and (koef[0]>0):
		return "Система на колебательной гнанице устойчивости (по Гурвицу)"
	if (koef[2] < 0) or (koef[1]*koef[2]-koef[0]*koef[3] < 0) or (koef[0]<0):
		return "Система неустойчива (по Гурвицу)"


if __name__ == '__main__':
	A = [[0,1,0],[0,0,1],[-1,-1,-3]]
	print("Матрица А:")
	print(out(A))
	print('\n')
	print(gur(A))
