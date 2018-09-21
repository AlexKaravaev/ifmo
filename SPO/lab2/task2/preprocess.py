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

def preprocess():

    ### Read spreadsheet id from file
    f = open("spreadsheetId.txt", "r")
    ssId = f.read()

    ### Get x and y from table and preproccess data
    result = service.spreadsheets().values().get(spreadsheetId=ssId,
                                                range="1!A1:Y"+str(variant_num)).execute()

    values = result.get('values', [])
    print(len(values))
    print(len(values[0]))
    values = [[float(values[i][j].replace(",", ".")) if values[i][j] != '' else -100 for j in range(len(values)-1)] for i in range(len(values)-1)]
    values = np.array(values)

    return values
