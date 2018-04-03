#!usr/bin/env python

'''
Current working of the script only utilizes the gspread and oauth2 libraries to make a call to the API
Other than using the API, the script does not do much.

Input : Script should run on an inputted DF (most likely a pandas DF)
Output : A modified Google Docs sheet, with raw data and data analysis columns
'''

from __future__ import print_function
import datetime

start_time = datetime.datetime.now() #Testing runtime

#import googleapiclient.discovery as d_api #stands for drive api; to help manage files and whatnot
import pandas as pd
from clean import clean
import pprint

# ------------------- Google Imports ----------------------#

import httplib2  #library to make https requests (internet connectivity)
import os        #OS lib - pretty self explanitory

import gspread                                #separate google api to help manage spreadsheets

from googleapiclient import discovery         #Various authentication libraries and drive api's
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import_time = datetime.datetime.now()

# -------------- Credentials generator ---------------------#

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
        flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'AS Data Management'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
    Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                        'drive-python-quickstart.json')

    else:
        credential_path = os.path.join(credential_dir,
                                       'client_secret.json')

    store = Storage(credential_path)
    credentials = store.get()

    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    flow.user_agent = APPLICATION_NAME
    
    if flags:
        credentials = tools.run_flow(flow, store, flags)
    else: # Needed only for compatibility with Python 2.6
        credentials = tools.run(flow, store)
    print('Storing credentials to ' + credential_path)
    return credentials

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


def create_csv(sheet_names, csv_name):
    
    '''
    Writes raw data and cleaned data to the two given spreadsheets
    Args:
        sp_name_1(`string`): Name of the spreadsheet to write raw data to
        sp_name_2(`string`): Name of the spreadsheet to write clean data to
        csv_name(`string`): Filepath to the csv the raw data comes from
    '''

    #Sheet names
    raw_name    = sheet_names[0]
    clean_name  = sheet_names[1]



#----------------            Main            ----------------------- #

def __main__():
    raw_sheet_name, clean_sheet_name = csv_names()

    csv_filepath = 'approval_polllist.csv' 

    #Credential authentication and API initialization
    credentials = get_credentials()
    http        = credentials.authorize(httplib2.Http())
    drive       = discovery.build('drive', 'v3', credentials=credentials)


    raw_data   = pd.read_csv(csv_filepath)
    print("CSV READ AND CONVERTED TO DF")
    clean_data = clean(raw_data) 
    print("CLEANED DF CREATED")

    raw_sp_body   = raw_data.to_json()
    clean_sp_body = clean_data.to_json()

    #print("\n", pprint.pprint(raw_sp_body))
    #print("\n", pprint.pprint(clean_sp_body))

#    doesn't work for whatever reason
    create_raw   = drive.files().create(body=raw_sp_body)
    create_clean = drive.files().create(body=clean_sp_body)

    response_one = create_raw.execute()
    response_two = create_clean.execute()
__main__()

#----------------      Runtime Analsysis     ------------------------ #

end_time = datetime.datetime.now()

print ("\nImport runtime is :", import_time - start_time)
print ("Script runtime of :", end_time - import_time)
print ("TOTAL RUNTIME OF  :", end_time - start_time)
