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


# ------------------- Google Imports ----------------------#

import httplib2  #library to make https requests (internet connectivity)
import os        #OS lib - pretty self explanitory

import gspread                          #separate google api to help manage spreadsheets
from apiclient import discovery         #Various authentication libraries and drive api's
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


def create_csv(sheet_names, csv_name, oauth_obj):
    
    '''
    Writes raw data and cleaned data to the two given spreadsheets
    Args:
        sp_name_1(`string`): Name of the spreadsheet to write raw data to
        sp_name_2(`string`): Name of the spreadsheet to write clean data to
        csv_name(`string`): Filepath to the csv the raw data comes from
    '''

#----------------            Main            ----------------------- #

def __main__():

    credentials = get_credentials()
    http        = credentials.authorize(httplib2.Http())
    service     = discovery.build('drive', 'v3', http=http)


__main__()

#----------------      Runtime Analsysis     ------------------------ #

end_time = datetime.datetime.now()

print ("\nImport runtime is :", import_time - start_time)
print ("Script runtime of :", end_time - import_time)
print ("TOTAL RUNTIME OF  :", end_time - start_time)
