#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 10:37:51 2019

@author: jean-christopheperrin
"""

import pickle
import os.path
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def get_credentials():
    """ This function gets the credentials needed to access the google sheets
    API. Copied from [this link](https://developers.google.com/sheets/api/quickstart/python)
    """
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def import_spreadsheet(creds):
    """ Reads raw data from the spreadsheet """
    service = build('sheets', 'v4', credentials=creds)
    
    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '19jEFs1IXQjO0gdcB2lQuQlwc76rK_eX2K2WyEcB1ox0'
    SAMPLE_RANGE_NAME = 'scores!A1:G65'

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    df = pd.DataFrame(values[1:], columns=values[0])
    return df

def main():
    creds = get_credentials()
    df = import_spreadsheet(creds)
    df.to_csv(path_or_buf='../data/2019_bestAlbums.csv')

if __name__ == '__main__':
    main()