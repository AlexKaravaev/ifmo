import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import numpy


variant_num = 25

### STUFF TO LOGIN ###
CREDENTIALS_FILE = 'credentials.json'  # имя файла с закрытым ключом

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',
                                                                                  'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)


### Create spreadsheet
spreadsheet = service.spreadsheets().create(body = {
    'properties': {'title': 'MNK', 'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': '1',
                               'gridProperties': {'rowCount': variant_num, 'columnCount': 2}}}]
}).execute()

### Give permissions to write
driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth)
shareRes = driveService.permissions().create(
    fileId = spreadsheet['spreadsheetId'],
    body = {'type': 'user', 'role': 'writer', 'emailAddress': 'alexkaravev@gmail.com'},  # доступ на чтение кому угодно
    fields = 'id'
).execute()

### write spreadsheet id to file
f = open("spreadsheetId.txt","a")
f.write(spreadsheet['spreadsheetId'])
f.close()
print("Link to table is: https://docs.google.com/spreadsheets/d/{}".format(spreadsheet['spreadsheetId']))
