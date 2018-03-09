#!usr/bin/env python

'''
Current working of the script only utilizes the gspread and oauth2 libraries to make a call to the API
Other than using the API, the script does not do much.

Input : Script should run on an inputted DF (most likely a pandas DF)
Output : A modified Google Docs sheet, with raw data and data analysis columns
'''
import datetime
import googleapiclient.discovery as d_api #stands for drive api; to help manage files and whatnot
import pandas as pd
import gspread  #separate google api to help manage spreadsheets
from oauth2client.service_account import ServiceAccountCredentials
from clean import clean

start_time = datetime.datetime.now() #Testing runtime

'''
The majority of runtime happens for API calls.
Stack overflow says we should try multiprocessing and
calling API's in parallel
'''

#---------------- API Calls to manage spreadsheet ------------------#

scope = ['https://spreadsheets.google.com/feeds', "https://www.googleapis.com/auth/drive"] #very dangerous scope DO NOT deploy to production
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)



#----------------       File Management     -------------------------#


# Find a workbook by name and open the first sheet
# Make sure you use the right name here.

def create_csv(sp_name_1, sp_name_2, csv_name):
    
    '''Writes raw data and cleaned data to the two given spreadsheets
    Args:
        sp_name_1(`string`): Name of the spreadsheet to write raw data to
        sp_name_2(`string`): Name of the spreadsheet to write clean data to
        csv_name(`string`): Filepath to the csv the raw data comes from
    '''
    
    sheet_one = client.open(sp_name_1).sheet1   #Named the google docs sheet "Raw Data Spreadsheet"
    sheet_two = client.open(sp_name_2).sheet1
    print ("Connecting to sheets to edit --- DONE")

    raw_data = pd.read_csv(csv_name)
    sheet_one.import_csv(raw_data.to_csv())
    print("Printing CSV to Google sheet --- DONE ")

    clean_data = clean(raw_data)
    print("Cleaning data --- DONE")
    sheet_two.import_csv(clean_data.to_csv())   #TODO: change this to write to a different spreadsheet 
    print("Printing clean CSV to Google sheet --- DONE")


#----------------      Runtime Analsysis     ------------------------ #

end_time = datetime.datetime.now()
print ("RUNTIME OF :", end_time - start_time)
