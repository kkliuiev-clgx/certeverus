"""
PROTOTYPE -- THE DATA WILL GO THROUGH THE IM AND EM WHEN USING DJANGO
This is how we will ingest sales data for the sales demo.
It is a protype for the ingestion of other client data.

Created on Fri Oct  9 08:02:08 2020

@author: michaelprinci
"""

# import os

import pandas as pd
try:
    from cvai import EncapsulationManager as em, transformation_manager as tm
except ImportError:
    import EncapsulationManager as em
    import transformation_manager as tm

def get_sales_demo_data():
    ''' this should draw from a text file for the attributes
    and the RAW client data file can be placed in the folder'''
    target = (r'./cvai/data/Ingram Raw POS Data.csv')
    driver_target = (r'./cvai/data/IngramRawDrivers.csv')
    dframe = pd.read_csv(target, parse_dates=True)
    driverfile = pd.read_csv(driver_target)

    # print(df)

    dframe['Date'] = pd.to_datetime(dframe['Date'])
    dframe = dframe.set_index('Date')
    dframe['Scenario'] = "ACTUALS"

    mdfmerged = dframe
    return mdfmerged, driverfile


''' THIS IS NOT GOING THROUGH THE EM - ALlows for loading data directly,
but there is no connection to the front end '''
# drivers, dfc = em.pass_prepared_data()
# print('FROM EM\n',drivers, dfc)

dfc, drivers = get_sales_demo_data()
num = drivers.Metric.dropna().to_list()
den = drivers.Denominator.dropna().to_list()

pd.set_option('display.max_rows', None)

drive_x2, num_x2, den_x2  = tm.create_drivers(dfc, drivers, driver_parent=drivers['Parent'], attributes=['Scenario'], resample_period='A')

# print('DRIVEX:\n',drive_x2, "\n\n",drive_x2.columns,'\nNUMX:\n',num_x2,"\n\n",num_x2.columns, '\nDENX:\n',den_x2, "\n\n",den_x2.columns) 

pd.reset_option('display.max_rows', None)
print(dfc.columns)



