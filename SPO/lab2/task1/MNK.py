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


def linRegr(x,y):
    n = variant_num
    a = (n * np.sum(np.multiply(x,y)) - np.sum(x)*np.sum(y))/(n * np.sum(np.square(x)) - np.square(np.sum(x)))
    b = (np.sum(y) - a * np.sum(x)) / n
    return a,b


if __name__ == '__main__':
    ### Read spreadsheet id from file
    f = open("spreadsheetId.txt", "r")
    ssId = f.read()

    result = service.spreadsheets().values().get(spreadsheetId=ssId,
                                                range="1!A1:B"+str(variant_num)).execute()
    values = result.get('values', [])
    values = [[float(value[0].replace(",",".")),float(value[1].replace(",","."))] for value in values]
    values = np.array(values)
    x,y = values[:,0],values[:,1]

    a,b = linRegr(x,y)
    print("Коэфициенты аппр.прямой y = k*x + b: k={}, b = {}".format(a,b))
    plt.plot(x,y,'g^')
    X_range = range(-100,100)
    plt.plot(range(-100,100), a*X_range + b)
    plt.show()
