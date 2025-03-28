from googleapiclient.discovery import build
from google.oauth2 import service_account

# Define the scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/spreadsheets.readonly','https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = r"C:\Users\Ashish\Documents\Sales Order Scalable - Project\database_connection\Sheet_api_key.json"

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID of the spreadsheet to update.
SPREADSHEET_ID = '1ZVAH1usLFhdjoBIh2Bq2CUKHwE6f4A4nT5ULGqsKRU0'

# The range of cells to update.
RANGE_NAME = 'Products!A2:F'

# How the input data should be interpreted.
VALUE_INPUT_OPTION = 'RAW'  # 'USER_ENTERED'

column_row = ['Product ID','Product Category','Product Name','Price','Discount','Avilablity']

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                            range=RANGE_NAME).execute()
values = result.get('values', [])

def send_data_for_firebase():
    if not values:
        print('No data found.')
    else:
        print('Data found:')
        result_array = []
        for row in values:
            # Process each row of data 
            d1 = {}
            for i in range(len(row)):
                data = row[i]
                key = column_row[i]
                d1[key] = data
            result_array.append(d1)
    return result_array
            # print(row) 