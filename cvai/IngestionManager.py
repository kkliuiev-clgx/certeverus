# -*- coding: utf-8 -*-
"""
This is how we will manage data ingestion


Created on Sat Jul  4 06:22:43 2020

@author: michaelprinci
"""

import os
import pandas as pd

try:
    from cvai import gdsingestion as gds
except ImportError: 
    from cvai import gdsingestion as gds
# import localingestion as li

def readUserInput():

    InputNote = "Input a file from either Google Drive or local"
    print(InputNote)
    userInput = "Google Drive" #input('What type? (Google Drive or local)   ')
    print(userInput)
    return userInput

def selectSource(userchoice, **kwargs):
    try:
        from cvai import gdsingestion as gds
    except ImportError:
        
        from cvai import gdsingestion as gds

    if userchoice == "Google Drive":
        df = gds.gdsLoader()
        return df  #replace with a call to gds manager

    if userchoice == "local":
        print("from IM: You chose local from server")
        try:
            import s3fs
            from cvai import planIngestion as pi
            from django.conf import settings
            s3 = s3fs.S3FileSystem(
                anon=False,
                key=settings.AWS_ACCESS_KEY_ID,
                secret=settings.AWS_SECRET_ACCESS_KEY
            )
            client = kwargs.get("client")
            client_file = client.get_files("combined_data")[0]
            file = client_file.file
            name, ext = client_file.get_file_info()
            if ext == "csv":
                if client.get_storage_backend() == "file":
                    df = pd.read_csv(open(file.path, 'r'))
                elif client.get_storage_backend() == "s3":
                    s3_url = f"{file.storage.bucket_name}/{file.name}"
                    df = pd.read_csv(s3.open(s3_url))
            elif ext in ["xls", "xlsx"]:
                if client.get_storage_backend() == "file":
                    df = pd.read_excel(open(file.path, 'rb'))
                elif client.get_storage_backend() == "s3":
                    s3_url = f"{file.storage.bucket_name}/{file.name}"
                    df = pd.read_excel(s3.open(s3_url))

            # Update ingestion status
            client_file.ingestion_status = "processed"
            client_file.save()

        except ImportError:
            df = pd.read_excel('combinedDatalive.xlsx')
        return  df

    print ("This not a correct type, please try again.")
    readUserInput()
    return

def readDriverInput():
    DriverNote = "Input a driver file"
    print(DriverNote)
    driverInput = 'local' #input('What type? (remote or local)   ')
    print(driverInput)
    return driverInput

def selectDriverSource(driverchoice, **kwargs):
    if driverchoice == "remote": return print('Not Yet Available') #replace with call to gds manager
    if driverchoice == "local":
        try:
            from cvai import driverIngestion as di
        except ImportError:
            import driverIngestion as di

        drivers = di.getDrivers(**kwargs)
        return drivers
    print ("This not a correct type, please try again.")
    readDriverInput()
    return

def readPlanInput():
    PlanNote = "Input a plan file"
    print(PlanNote)
    planInput = 'local' #input('What type? (remote or local)   ')
    print(planInput)
    return planInput

def selectPlanSource(planchoice, **kwargs):
    if planchoice == "remote": return print('Not Yet Available') #replace with a call to gds manager
    if planchoice == "local":
        targetdir = ""
        try:
            from cvai import planIngestion as pi
        except ImportError:
            import planIngestion as pi
            # targetdir = 'C:\\Users\\jordy\\CV\\GitHub\\CerteVerus-AI-MVP\\cvai'
            targetdir = r'D:\Dropbox\new model (TSC)\Data for FHMS\\'

        plandf = pi.Load_Data_from_folder_for_OPX(targetdir, **kwargs)
        return plandf

    print ("This not a correct type, please try again.")
    readDriverInput()
    return

def GetInput(**kwargs):
    source = kwargs.get("source")
    if source:
        drivers = selectDriverSource(source, **kwargs)
        dataframe = selectSource(source, **kwargs)
        plan = selectPlanSource(source, **kwargs)
        return dataframe, drivers, plan

    driverchoice = readDriverInput()
    drivers = selectDriverSource(driverchoice)

    userchoice = readUserInput()
    dataframe = selectSource(userchoice)

    planchoice = readPlanInput()
    plan = selectPlanSource(planchoice)
    print("PLAN:\n", plan)
    return dataframe, drivers, plan
