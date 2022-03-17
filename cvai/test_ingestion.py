'''  '''
import pickle
import unittest
import json
import dropbox
# import plotly

import pandas as pd
import pytest
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import gspread

import cvai.gdsingestion as gds
import cvai.import_from_Dropbox as idb
import cvai.salesforce_api as sfa
global gc

from simple_salesforce import Salesforce
import requests
import csv
from io import StringIO




class TestGoogleDrive:
    ''' '''
    def test_readFromFolder(self):
        '''      '''
        # Setup
        folderID = '1TMxwneRtYX_tMKyt-uuy-Ga3uIzqnV2w'
        expected_filelist = ['1eBiGpbqq10L6kHVKy58Cx63Mio8kQVjFFk3fztt4VEA']
        # Exercise
        calculated_filelist = gds.readFromFolder(folderID)
        print(calculated_filelist)
        # Validate
        assert calculated_filelist == expected_filelist
        # Teardown

    def test_getGoogleSheet(self):      
        '''      '''
        # Setup
        spreadsheet_key = '1eBiGpbqq10L6kHVKy58Cx63Mio8kQVjFFk3fztt4VEA'
        gc = gds.GetCredentials()
        expected_book = 'Patient Available Hours - final'
        # Exercise
        calculated_book = gds.GetGoogleSheet(spreadsheet_key)
        # Validate
        assert calculated_book.title == expected_book
        # Teardown
        # request.config.cache.set("GoogleSheet", calculated_book.get_worksheet(0))

    def test_GetData_from_goggle(self):
        '''      '''
        # Setup
        spreadsheet_key = '1eBiGpbqq10L6kHVKy58Cx63Mio8kQVjFFk3fztt4VEA'
        gc = gds.GetCredentials()
        # book = request.config.cache.get("GoogleSheet", None)
        book = gds.GetGoogleSheet(spreadsheet_key)
        expected_df = pd.read_json(r'./cvai/data/google_dataframe.json')
        # expected_df['Date'] = expected_df['Date'].dt.strftime('%m/%d/%Y').str.lstrip("0").replace(" 0", " ")
        # Exercise
        calculated_df = gds.GetData(book)
        calculated_df.Date = pd.to_datetime(calculated_df.Date)
        cols = calculated_df.columns.drop('Date')
        calculated_df[cols] = calculated_df[cols].apply(pd.to_numeric, errors='ignore')
        # calculated_df.to_json(r'./cvai/data/google_dataframe.json')
        # Validate
        assert pd.testing.assert_frame_equal(calculated_df, expected_df, check_dtype=False) is None
        # Teardown

    def test_gdsLoader(self):
        '''      '''
        # Setup
        expected_df = pd.read_json(r'./cvai/data/google_sheets_expected.json',orient = 'table').set_index('Date')

        # Exercise
        calculated_df = gds.gdsLoader('1TMxwneRtYX_tMKyt-uuy-Ga3uIzqnV2w')
        # calculated_df.to_json(r'./cvai/data/google_sheets_expected.json',orient = 'table')
        # Validate
        assert pd.testing.assert_frame_equal(calculated_df, expected_df) is None
        # Teardown


class TestDropbox:
    ''' '''
    def test_read_from_dropbox_folder(self):
        '''      '''
        # Setup
        expected_filelist = ['/VIVA EVE Plan (2020-2025).xlsx', '/READ ME.txt', '/FHMS_Drivers_v3.csv']
        # Exercise
        calculated_filelist = idb.read_from_Dropbox_folder("Si2kikU8Lu8AAAAAAAAAAYJkTGm90CtD54N3x3VhJpOwBwnA8Rtu3OkHPCyQYvVe")
        # Validate
        assert calculated_filelist == expected_filelist
        # Teardown

    def test_get_dropbox_file_contents(self,FHMS_drivers):
        '''      '''
        # Setup
        token = 'Si2kikU8Lu8AAAAAAAAAAYJkTGm90CtD54N3x3VhJpOwBwnA8Rtu3OkHPCyQYvVe'
        path = '/FHMS_Drivers_v3.csv'
        dbx = dropbox.Dropbox(token)
        expected_df= FHMS_drivers

        # Exercise
        stream = idb.get_dropbox_file_contents(path)
        stream.seek(0)
        calculated_df = pd.read_csv(stream)
    
        # Validate
        assert pd.testing.assert_frame_equal(calculated_df,expected_df) is None #how do I save a stream object?
        # Teardown
class TestSFDCAPI:
    def test_sfdc_ingestion(self):
        '''      '''
        # Setup
        user='steve.stark@certeverus.ai'
        pw='GoArmy#211'
        sec_token='u0biHPkgRK9OVQGi0t6E2zqq2'
        rep_id = '00O3p000005ap9lEAA' 
        org = 'https://certeverus.lightning.force.com/'
        expected_df = pd.read_json(r'./cvai/data/sfdc_report_expected.json')

        # Exercise
        calculated_df = sfa.salesforce_data(user, pw, sec_token, rep_id, org)
        # Validate
        assert pd.testing.assert_frame_equal(calculated_df,expected_df)
        # Teardown
