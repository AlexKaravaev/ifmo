N = int(input("Enter N\n"))
Y = N / 24
S = A_1 = A_2 = A_3 = 0

while S != 1:
    A_1 = float(input("Enter probability for Dasha\n"))
    A_2 = float(input("Enter probability for Igor\n"))
    A_3 = float(input("Enter probability for Kirill\n"))
    S = A_1 + A_2 + A_3
    print("invalid probability sum") if S != 1.0 else 0

print("Answer ", (A_1 * Y) ** 300)
