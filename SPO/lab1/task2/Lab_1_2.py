chars = frozenset('0123456789i.+-')
Numbers = []
Complex = []
Real = []
Rational = []
Whole = []
Natural = []
Even = []
Odd = []
Prime = []

def getList():
        while True:
            x = str(input("Enter a number or press 's'\n"))
            if x == 's':
                print('\n', Numbers, '\n')
                break
            print("Incorrect input") if any((c not in chars) for c in x) else Numbers.append(x)

def checkComplex(x):
    Complex.append(x) if 'i' in x else Real.append(x)

def checkWhole(x):
    Whole.append(x) if 'i' not in x and '.' not in x else 0

def checkNatural(x):
    Natural.append(x) if ('-' or '0') not in x else 0

def checkEven(x):
    Even.append(x) if x % 2 == 0 else Odd.append(x)

def checkPrime(x):

    primes = [1, 2, 3, 5, 7, 11, 13, 17, 19, 23]

    is_prime = True if x in primes else False

    i = 5
    while (i ** 2 <= x):
        is_prime = False if (x % i == 0) or (x % (i + 2) == 0) else True
        i += 6

    Prime.append(x) if is_prime else 0


if __name__ == "__main__":
    getList()
    Rational = Real

    for i in range(len(Numbers)):
        checkComplex(Numbers[i])
        checkWhole(Numbers[i])
    for i in range(len(Whole)):
        checkNatural(Whole[i])
        checkEven(int(Whole[i]))
        checkPrime(int(Whole[i]))

    print("Complex\n", Complex)
    print("Real\n", Real)
    print("Rational\n", Rational)
    print("Whole\n", Whole)
    print("Natural\n", Natural)
    print("Even\n", Even)
    print("Odd\n", Odd)
    print("Prime\n", Prime)
