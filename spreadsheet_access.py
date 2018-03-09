#!usr/bin/env python

'''
Current working of the script only utilizes the gspread and oauth2 libraries to make a call to the API
Other than using the API, the script does not do much.

Input : Script should run on an inputted DF (most likely a pandas DF)
Output : A modified Google Docs sheet, with raw data and data analysis columns
'''

import datetime

start_time = datetime.datetime.now() #Testing runtime

import googleapiclient.discovery as d_api #stands for drive api; to help manage files and whatnot
import pandas as pd
import gspread  #separate google api to help manage spreadsheets
from oauth2client.service_account import ServiceAccountCredentials
from clean import clean

import_time = datetime.datetime.now()



'''
The majority of runtime happens for import calls
averaging somewhere between 5 - 7 seconds
'''

#---------------- API Calls to manage spreadsheet ------------------#
def authenticate():
    scope = ['https://www.googleapis.com/auth/drive'] #This is a very dangerous scope to call, this probably should not be pushed to deployment
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    print ("Connection authenticated")


#----------------       File Management     -------------------------#

#Returns MM-DD-YYYY
def name_file():
    date = datetime.date.today()
    date = str(date)
    date_list = date.split('-')
    date_list = date_list[::-1]
    tmp = date_list[0]
    date_list[0] = date_list[1]
    date_list[1] = tmp
    date_str = "-".join(date_list)
    print ("Date :", date_str)
    return

#TODO: Implement function to create new spreadsheets with correct names
def initialize_csv(sp_type):
    clean = "Clean Datasheet "
    raw   = "Raw Datasheet "

    if sp_type == "clean":
        clean += name_file()
        new_clean_sheet = client.create(clean)
        return new_clean_sheet
    else:
        raw += name_file()
        new_raw_sheet = client.create(raw)
        return raw_clean_sheet


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


#----------------            Main            ----------------------- #

def __main__():
    authenticate()
    name_file()

__main__()

#----------------      Runtime Analsysis     ------------------------ #

end_time = datetime.datetime.now()

print ("\nImport runtime is :", import_time - start_time)
print ("Script runtime of :", end_time - import_time)
print ("TOTAL RUNTIME OF  :", end_time - start_time)
