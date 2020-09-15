import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
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

    ### Read range from user
    Range = [int(x) for x in input('Введите диапазон значений x и y через запятую: ').split(',')]

    ### Update table
    results = service.spreadsheets().values().batchUpdate(spreadsheetId = ssId, body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
        {"range": "1",
         "majorDimension": "ROWS",
         "values": [[random.uniform(Range[0],Range[1]), random.uniform(Range[0],Range[1])] for i in range(variant_num)]}
    ]
    }).execute()
