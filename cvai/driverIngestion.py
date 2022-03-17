#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 13:09:37 2020

@author: michaelprinci
"""
import os
import pandas as pd

def getDrivers(**kwargs):
    try:
        import s3fs
        from django.conf import settings
        s3 = s3fs.S3FileSystem(
            anon=False,
            key=settings.AWS_ACCESS_KEY_ID,
            secret=settings.AWS_SECRET_ACCESS_KEY
        )

        client = kwargs.get("client")
        client_file = client.get_files("driver")[0]
        file = client_file.file

        name, ext = client_file.get_file_info()
        if ext == "csv":
            if client.get_storage_backend() == "file":
                drivers = pd.read_csv(open(file.path, 'r'))
            elif client.get_storage_backend() == "s3":
                s3_url = f"{file.storage.bucket_name}/{file.name}"
                drivers = pd.read_csv(s3.open(s3_url))
        elif ext in ["xls", "xlsx"]:
            if client.get_storage_backend() == "file":
                drivers = pd.read_excel(open(file.path, 'rb'))
            elif client.get_storage_backend() == "s3":
                s3_url = f"{file.storage.bucket_name}/{file.name}"
                drivers = pd.read_excel(s3.open(s3_url))

        # Update ingestion status
        client_file.ingestion_status = "processed"
        client_file.save()

    except ImportError:
        drivers = pd.read_csv(r'./data/fhmsdriver.csv')
    return drivers
