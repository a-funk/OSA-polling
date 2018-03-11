#!usr/bin/env python

'''
Current working of the script only utilizes the gspread and oauth2 libraries to make a call to the API
Other than using the API, the script does not do much.

Input : Script should run on an inputted DF (most likely a pandas DF)
Output : A modified Google Docs sheet, with raw data and data analysis columns
'''

import datetime

start_time = datetime.datetime.now() #Testing runtime

#import googleapiclient.discovery as d_api #stands for drive api; to help manage files and whatnot
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
    return client


#----------------       File Management     -------------------------#

#Returns MM-DD-YYYY
#Helper function that is called in initialize_csv
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
    return date_str

#Returns names of 2 spreadsheets to create
def csv_names():
    
    clean   = "Clean Datasheet "
    raw     = "Raw Datasheet "

    #Determines Google Spreadsheet name if sheet is clean
    clean += name_file()
    print("Sheet Names Initalized :",clean)

    #Determines Google Spreadsheet name if sheet is raw
    raw += name_file()
    print("Sheet Names Initialized :",raw)

    return (raw, clean)


def create_csv(sheet_names, csv_name, oauth_obj):
    
    '''
    Writes raw data and cleaned data to the two given spreadsheets
    Args:
        sp_name_1(`string`): Name of the spreadsheet to write raw data to
        sp_name_2(`string`): Name of the spreadsheet to write clean data to
        csv_name(`string`): Filepath to the csv the raw data comes from
    '''
    client = oauth_obj

    raw_sheet_name, clean_sheet_name = sheet_names

    raw_sheet   = client.create(raw_sheet_name)   #Named google sheet "Raw Datasheet   + Date"
    clean_sheet = client.create(clean_sheet_name) #Names google sheet "Clean Datasheet + Date"
    print ("Connecting to sheets to edit --- DONE")

    raw_data = pd.read_csv(csv_name)
    client.import_csv(raw_sheet.id, raw_data.to_csv())
    print("Printing CSV to Google sheet --- DONE ")

    clean_data = clean(raw_data)
    print("Cleaning data --- DONE")
    clean_csv = clean_data.to_csv()
    client.import_csv(clean_sheet.id, clean_csv)   #TODO: change this to write to a different spreadsheet 
    print("Printing clean CSV to Google sheet --- DONE")

#----------------            Main            ----------------------- #

def __main__():
    oauth = authenticate()  #returns an oauth object needed to verify the connection to make api calls
    names = csv_names()     #returns a tuples of strings; ("Clean Datasheet + Date", "Raw Datasheet + Date")

    create_csv(names, 'approval_polllist.csv', oauth) #initalizes 2 spreadsheets on google drive with respective clean/raw names. 

__main__()

#----------------      Runtime Analsysis     ------------------------ #

end_time = datetime.datetime.now()

print ("\nImport runtime is :", import_time - start_time)
print ("Script runtime of :", end_time - import_time)
print ("TOTAL RUNTIME OF  :", end_time - start_time)
