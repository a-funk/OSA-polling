#!usr/bin/env python

'''
Current working of the script only utilizes the gspread and oauth2 libraries to make a call to the API
Other than using the API, the script does not do much.

Input : Script should run on an inputted DF (most likely a pandas DF)
Output : A modified Google Docs sheet, with raw data and data analysis columns
'''

import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from clean import clean

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.

def create_csv(sp_name, csv_name):
    sheet_one = client.open(sp_name).sheet1   #Named the google docs sheet "Raw Data Spreadsheet"
    
    raw_data = pd.read_csv(csv_name)
    sheet_one.import_csv(raw_data.to_csv())
    
    clean_data = clean(raw_data)
    sheet_one.import_csv(raw_data.to_csv())   #TODO: change this to write to a different spreadsheet 
