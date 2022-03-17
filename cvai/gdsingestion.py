#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is how we will access data from Google Data Sheets in a shared folder


Created on Sat Jul  4 06:22:18 2020

@author: michaelprinci
"""

import os.path
import pickle
import time


import numpy as np
import pandas as pd
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import gspread
try:
    import ingest_local_textdata as ilt
    import ingest_financial_statement as ift
except ImportError:
    from cvai import ingest_local_textdata as ilt
    from cvai import ingest_financial_statement as ift



# If modifying these scopes, delete the file token.pickle.

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/spreadsheets'
    ]
# folderID = '1TMxwneRtYX_tMKyt-uuy-Ga3uIzqnV2w' # get folderID

def readFromFolder(folderID):
    '''
    writes all file IDs from a specific folder to a list
    '''
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r'./cvai/client_secrets.json', SCOPES) #change to service acct creds for cloud account
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    page_token = None

    fileList = []
    fileDict = {}
    while True:
        service = build('drive', 'v3', credentials=creds)
        folder = service.files().list(q="",  # pylint: disable=maybe-no-member
                                          spaces='drive',
                                          fields='nextPageToken, files(id, name, parents)',
                                          pageToken=page_token).execute()
        # folder2 = service.files().list(q="name contains 'xlsx' and name contains 'Drivers'",
        #                                   spaces='drive',
        #                                   fields='nextPageToken, files(id, name, parents)',
        #                                   pageToken=page_token).execute()
        print(folderID)
        for file in folder.get('files', []):
            # print(file,folderID)
            fileDict[file.get('id')] = file.get('parents')
            page_token = folder.get('nextPageToken', None)
        if page_token is None:
            break
        fileList = [k for (k,v) in fileDict.items() if v is not None and folderID in v]
        # print(f'{fileList =}')
        return fileList

def GetCredentials(): 
    '''
    Create function to get credentials
    '''
    from oauth2client.service_account import ServiceAccountCredentials
    global gc
    scope = ['https://www.googleapis.com/auth/spreadsheets'] #Sets Scope for Google Sheets

    credentials = ServiceAccountCredentials.from_json_keyfile_name(r'./cvai/service_account_GS.json', scope)
    gc = gspread.authorize(credentials) # authorizes credentials for Google sheets
    return gc

def GetGoogleSheet(spreadsheet_key): 
    '''
    Creates function for getting Google sheet
    '''
    book = gc.open_by_key(spreadsheet_key) # set spreadsheet to book
    return book

def GetData(book):
    '''
    Consolidates Data from Google Sheets
    '''
    worksheet_list = book.worksheets()  #get list of worksheets in Google Book
    dfmerged = pd.DataFrame() #initiailize the dataframe

    for num,i in enumerate(worksheet_list):
        # print("this is -",num, "from ", i )
        worksht = book.get_worksheet(num)
        name = worksht.title
        table = worksht.get_all_values()
        df = pd.DataFrame(table[1:], columns=table[0])
        df['Scenario'] = name
        dfmerged = pd.concat((dfmerged,df),axis = 0, sort=False)
        print(name,"tab loaded", i, num)
    # dfmerged['Date'] =dfmerged['Date'].astype('datetime64') #sets data as a datetime /// FHMS Specific -  can be deferred or call ilt.set_date_columns(data)
    dfmerged = dfmerged.applymap(lambda x: "NaN" if x=="" else x) #cleans blanks
    print("pausing")
    time.sleep(30)
    return dfmerged


#TODO #172 MOVE LoadDict TO THE IM

def LoadDict(files):
    '''
    Load Frames Dictionary with Google Sheets DataFrames
    '''
    frames_dict = {}
    mdfmerged = pd.DataFrame()
    for i in files: # step through each key value pair and develop an entry for each sheet
       # print(i)
        book = GetGoogleSheet(i) #TODO #169 dictionary loads book and data in loop - would this be different for any other source?
        data = GetData(book)
    #     df = data.melt(id_vars=(v[1]))
        frames_dict[i] = data
    return frames_dict



#TODO #171 MOVE UnPack to the EM?

def UnpackDict(frames_dict):
    '''
    Create a single Concated DataFrame from each of the Frames Dictionary Values
    '''
    mdfmerged = pd.DataFrame()
    for k,v in frames_dict.items(): # loop to step through each key value pair of frame dictionary
#         print("Item:", k,"\n Entry\n",v)
        mdfmerged =  pd.concat([mdfmerged,v], sort=False, ignore_index=True)#concatenates the frames
    mdfmerged['Procedures'] = mdfmerged['CPT'].apply(lambda x: None if x is np.nan  else '$ 1.0')
    # mdfmerged['Locations']= mdfmerged['Location'].apply(lambda x: None if x is np.nan  else '$ 1.0') 
    attribs=('Date', 'Location','Company','Service','Source','Medium','Provider','Payer','CPT','Visit ID')
    df = mdfmerged.melt(id_vars=(attribs))
    # print(df.columns)
    # df.to_csv(r"./catch/1melted.csv")
    df['Scenario'] = df['Sourced']
    df = pd.concat([df,count_unique_actuals(df, target = 'Location')])
    # if 'Providers' not in df['variable']:
    #     df = pd.concat([df,count_unique_actuals(df, target = 'Provider')])
    #     print('*********\n*********SKIPPED PROVIDER COUNT*********\n***************')
    # df.to_csv('2locs_and_providers.csv')
    df_trimmed = remove_future_actuals(df)
    # print(df.info())
    # print(df.variable.unique())
    # df.to_csv('3trimmed_dates.csv')
    return df_trimmed


#TODO #173 Move count_unique-actuals to either IM or EM

def count_unique_actuals(md, target='Provider'):
    ''' 
    Used to summarize/count unique actual items for FHMS specific data.  
    Should not be needed for new ingestion process
    '''
    md['Date'] = pd.to_datetime(md.Date)
    mdx = md.set_index('Date', drop=True)
    mdr= mdx.resample('M').nunique()
    mdr['variable']= target+"s"
    # mdr['Scenario']= scenario
    mdr['value'] = mdr[target]
    mdrf = mdr[['variable', 'value']].reset_index()
    return mdrf


#TODO #174 Move remove_future_actuals to either IM or EM

def remove_future_actuals(md):
    '''
    Remove extraneous Actuals (i.e. Future actuals) to prevent errors in transforamtions
    '''
    md['Date'] = pd.to_datetime(md['Date'])
    mdx = md.set_index('Date', drop=True)
    max_actuals_date = mdx.index[(mdx['variable'] == 'Free Cash Flow')&(mdx['value'].notnull())].max()
    print(str(max_actuals_date),"is max date for ACTUALS")
    md_trimmed = md[md['Date'] <= max_actuals_date]
    return md_trimmed


def gdsLoader(folderID = '1TMxwneRtYX_tMKyt-uuy-Ga3uIzqnV2w'):
    ''' 
    Control Method for getting Google Drive Data 
    '''

    # SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
    # 'https://spreadsheets.google.com/feeds']
    # folderID = '1TMxwneRtYX_tMKyt-uuy-Ga3uIzqnV2w' # get folderID
    # folderID = '1yU4qX-GKaVm8xXSP08Ze5W4k-jAtXxQY?lfhs=2' # 800BoardUp
    files = readFromFolder(folderID)
    gc = GetCredentials()
    frames_dict = LoadDict(files)
    print(frames_dict)
    df = ilt.unpack_dictionary(frames_dict) #TODO #175 Should we do our unpacking in the EM?
    currency_cols = ['Cost', 'Unit Cost']
    for i in currency_cols:
        df = ift.clean_currency(df,i)
    print(df)
    df.to_csv('inventory_data.csv')
    return df


# gdsLoader(folderID='1QH1sI1ugr22fH3NPD1Bq6vlA1AhP3jE-') # PT PLUS
# gdsLoader('1yU4qX-GKaVm8xXSP08Ze5W4k-jAtXxQY') #800BOARDUP
# gdsLoader(folderID='1IAkIGJrwkDoXEVHd8UNDrFdGHxtcvWED') #Accordion_inventory
# gdsLoader(folderID='1iA7rcIhU-HYNyqj2-nyxSF0Wi3SWr-1g') #Accordion_sourcing
# print()
