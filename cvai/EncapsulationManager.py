    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is how we will encapsulate, cleanse,and fill any data issues


Created on Sat Jul  4 11:21:50 2020

@author: michaelprinci
"""

try:
    import cvai.IngestionManager as im
except ImportError:
    from cvai import IngestionManager as im

import os
import pandas as pd
# import numpy as np


def cleanData(df):
    '''
    Clean the separate dataframes together and clean the value field #TODO #179 Need to run the plan through the cleaning process too
    '''
    # df.to_csv(r'./catch/fhms_preclean.csv')
    print('from EM: Start Cleaning Process')
    # print(df, "first time")
    # df['value'] =df['value'].astype(str)
    # df['value'] = df['value'].map(lambda x:x.replace('null',""))  #ADDED TO ADDRESS NULLs
    # print(df, "Second time")
    print('Cleaning - Dropping NAs')
    if 'value' in df.columns:
        df['value'] = df['value'].astype(str)
        print('cleaned S1 - Dropped NAs')
        df['value'] = df['value'].map(
            lambda x: x.lstrip('$ ').rstrip().replace(',', '').strip(')').replace('(', '-'))#cleans str
        print('cleaned S2 - cleaned strings')
#         print ('cleaned S3')
        nan_value = float("NaN")
        # Convert NaN values to empty string
        df['value'] = df['value'].replace("", nan_value, inplace=False)
        df['value'] = df['value'].replace("None", nan_value, inplace=False)
        df['value'] = df['value'].astype(float) # Convert values to float
        df = df.dropna(subset=['value']).reset_index()#cleans strings for NaNs-drop blanks in value()
    print('cleaned S4')
    print('cleaned S5 - values as float')
    # df['Scenario'] = "ACTUALS" 
    # # Adds column for Scenario label - Needs to be dynamic
    print('cleaned S6 - added scenario name')
    # print("S6:\n",df)
    print('***Data Loaded, Cleansed, and Saved to Database.  You can refresh ***')
    #df.to_excel("consolData.xlsx",na_rep="")
    return df

def CombineData(df, plan):
    ''' This function combines the Plan and Actual datasets '''
    print('Combining plan and actuals')
    df = df.append(plan)
    print("data combined")
    return df

def pass_prepared_data(**kwargs):
    '''This function builds the database and/or writes to csv for local use'''
    source = kwargs.get("source")
    engine = kwargs.get("engine")
    client = kwargs.get("client")
    save_data_to = kwargs.get("save_data_to", "csv")
    print('Passing Data out of Encapsulation Manager')
    if not os.path.isfile('dfcleaned.csv'):
        print('Getting data from Client Files on Django Admin EM70')
        df, drivers, plan = im.GetInput(source=source, client=client)#getting data from InputManager
        # print(df, "/n*****/n", plan)
    else:
        print('Reading Locally EM74')
        drivers = pd.read_csv('drivers.csv')
        df = pd.read_csv('dfcleaned.csv', parse_dates=True, index_col='Date')
        df = df.set_index('Date')
    dfclean = cleanData(df)
    dfclean=dfclean.set_index('Date')
    #dfclean.to_csv(r'./catch/actuals_for_loading.csv')
    # print("CLEAN:\n",dfclean)
    dfclean = CombineData(dfclean, plan) # combining the data into a single data frame
    # print(dfclean)
    #TODO #176 Create a method for Change_cols
    ''' THIS IS WHERE WE CAN GET THE CHANGE COLS FROM THE DRIVERS FILE '''
    if 'ChangeColumns' in drivers.columns:
        changecol = (drivers["ChangeColumns"].dropna())
        # print(changecol)
        change_columns = (changecol) # Creates list of all column headers TODO need to fix the columns
        dfclean[change_columns] = dfclean[change_columns].astype(str) 
    else:
        change_columns=()
    colnames = dfclean.columns
    if 'Unnamed: 0' in colnames:
        dfclean = dfclean.drop(['Unnamed: 0'], axis=1)
        # print('removed unnamed')
    # print(dfclean)
    # dfclean = dfclean.set_index('Date')
    save_data_to_db(save_data_to, dfclean,drivers, plan, client, engine)
    return drivers, dfclean, plan   


def save_data_to_db(save_data_to, dfclean,drivers, plan, client, engine):
    if save_data_to == "csv":
        dfclean.to_csv('dfclean.csv')
        drivers.to_csv('drivers.csv')
        plan.to_csv('plan.csv')
    elif save_data_to == "postgres":
        if client:  
            print("boom saving to dfclean: ", client.get_dfclean_table_name())
            print("boom saving to drivers: ", client.get_drivers_table_name())
            print("boom saving to plan: ", client.get_plan_table_name())
            dfclean.to_sql(client.get_dfclean_table_name(), engine, chunksize=500)
            print("*********** ACTUALS TABLE CREATED **********")
            engine.execute(
                """ALTER TABLE """ +client.get_dfclean_table_name()+ """ ALTER COLUMN "Date" SET DATA TYPE date USING CAST("Date" AS date);"""
                )
            drivers.to_sql(client.get_drivers_table_name(), engine, chunksize=500)
            print("*********** DRIVERS TABLE CREATED **********")
            plan.to_sql(client.get_plan_table_name(), engine, chunksize=500)
            print("*********** PLAN TABLE CREATED **********")            
            # Update ingestion status
            client.ingestion_status = "processed"
            client.save()
        else:
            dfclean.to_sql('dfclean', engine, chunksize=500)
            drivers.to_sql('drivers', engine, chunksize=500)
            plan.to_sql('plan', engine, chunksize=500)
