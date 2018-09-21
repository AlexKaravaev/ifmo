import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import numpy
import random

variant_num = 25

### STUFF TO LOGIN ###
CREDENTIALS_FILE = 'credentials.json'  # имя файла с закрытым ключом

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',
                                                                                  'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

if __name__ == '__main__':
    ### Read spreadsheet id from file
    f = open("spreadsheetId.txt", "r")
    ssId = f.read()

    Range = [1,30]
    vals = [[random.uniform(Range[0], Range[1]) for j in range(variant_num)] for i in range(variant_num)]
    random_indexes = [[random.randint(0,24),random.randint(0,24)] for i in range(11)]
    for i in range(10):
        vals[random_indexes[i][0]][random_indexes[i][1]] = ''
    print(vals)
    ### Update table
    results = service.spreadsheets().values().batchUpdate(spreadsheetId = ssId, body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
        {"range": "1",
         "majorDimension": "ROWS",
         "values": vals}
    ]
    }).execute()
