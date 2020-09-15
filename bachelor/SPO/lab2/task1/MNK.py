import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
import matplotlib.pyplot as plt

variant_num = 25


### STUFF TO LOGIN ###
CREDENTIALS_FILE = 'credentials.json'  # имя файла с закрытым ключом

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',
                                                                                  'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)


def linRegr(x, y):
    n = variant_num
    a = (n * np.sum(np.multiply(x, y)) - np.sum(x) * np.sum(y))/(n * np.sum(np.square(x)) - np.square(np.sum(x)))
    b = (np.sum(y) - a * np.sum(x)) / n
    return a, b

def polynomRegr(x, y, degree = 2):
    return np.poly1d(np.polyfit(x, y, deg = degree))

if __name__ == '__main__':
    ### Read spreadsheet id from file
    f = open("spreadsheetId.txt", "r")
    ssId = f.read()

    ### Get x and y from table and preproccess data
    result = service.spreadsheets().values().get(spreadsheetId=ssId,
                                                range="1!A1:B"+str(variant_num)).execute()

    values = result.get('values', [])
    values = [[float(value[0].replace(",", ".")), float(value[1].replace(",", "."))] for value in values]
    values = np.array(values)
    x,y = values[:,0], values[:,1]

    ### Do linear regression and calculate error
    a,b = linRegr(x, y)
    print("Коэфициенты аппр.прямой y = k*x + b: k={}, b = {}".format(a, b))
    plt.plot(x, y, 'g^')

    X_range = np.arange(x.min(), x.max())
    error_lin = sum([abs((a * x[i] + b) - y[i]) for i in range(len(x))])
    print("Ошибка в линейной аппроксимации: {}".format(error_lin))

    plt.plot(X_range, a*X_range + b, label = 'Линейная')

    ### Now do poly.regr until 5 degree
    for i in range(2, 7):
        poly_func = polynomRegr(x, y, i)
        error_poly = sum([abs(poly_func(x[i]) - y[i]) for i in range(len(x))])
        print("Ошибка в полиномиальной аппроксимации степени {}: {}".format(i, error_poly))
        plt.plot(X_range, poly_func(X_range), label = '{} степень'.format(i))

    ### Plot
    plt.legend(loc = 'upper left')
    plt.show()
