N = int(input("Enter N\n"))
Y = N / 24
A_1 = float(input("Enter probability for Dasha\n"))
A_2 = float(input("Enter probability for Igor\n"))
A_3 = float(input("Enter probability for Kirill\n"))

print("invalid probability sum") if A_1 + A_2 + A_3 != 1.0 else 0

print((A_1 * Y) ** 300)
