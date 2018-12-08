import xlsxwriter
import xlrd
import numpy as np
import matplotlib.pyplot as plt

workbook = xlsxwriter.Workbook('5_2.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write('A1', 'a(b)')
worksheet.write(1, 0, 1)
worksheet.write(2, 0, 2)
worksheet.write(3, 0, 3)
worksheet.write('B1', 'b(c)')
worksheet.write(1, 1, 1)
worksheet.write(2, 1, 2)
worksheet.write(3, 1, 3)
worksheet.write('C1', 'c(a)')
worksheet.write(1, 2, 1)
worksheet.write(2, 2, 4)
worksheet.write(3, 2, 9)

workbook.close()

file_location = "/Users/olegsouzdalev/Desktop/5_2.xlsx"
workbook = xlrd.open_workbook(file_location)
first_sheet = workbook.sheet_by_index(0)

# Graph a(b)
a_x = [first_sheet.cell_value(i + 1, 0) for i in range(3)]
a_y = [first_sheet.cell_value(i + 1, 1) for i in range(3)]

# Graph b(c)
b_x = [first_sheet.cell_value(i + 1, 1) for i in range(3)]
b_y = [first_sheet.cell_value(i + 1, 2) for i in range(3)]

# Graph c(b)
c_x = [first_sheet.cell_value(i + 1, 2) for i in range(3)]
c_y = [first_sheet.cell_value(i + 1, 0) for i in range(3)]

plt.plot(a_x, a_y)
plt.show()
plt.plot(b_x, b_y)
plt.show()
plt.plot(c_x, c_y)
plt.show()
