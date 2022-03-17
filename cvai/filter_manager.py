#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is how we will filter for the Source of Change for the Multifactor Drivers


Created on Sat Jul  4 12:25:10 2020

@author: michaelprinci
"""
import pandas as pd
import inspect

# *********** COLLECTING ATTRIBUTES *********


# def get_attributes(d_frame):
#     """ Gets Attributes for Detailed Views """
#     attribute_list = d_frame.columns.to_list()
#     # print(attribute_list)
#     return attribute_list



def chose_details(d_frame, attribs):
    """ Gets level of Aggregation for Analysis """

    if attribs == None:
        # print(f' AT {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} NO ATTRIBUTES', attribs)
        detail_choice = "A" #input('Detailed or Aggregate Data (D or A)? ')
        #this will be a passed param from utils.py
        attributes = ['variable', 'Scenario']
        attribute_choice = None
    else:
        # print(f' AT {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} Attributes =', attribs)
        detail_choice = 'D'
        # print(get_attributes(d_frame))
        attribute_choice = attribs

        #this will be a passed param from utils.py
        attributes = ['variable', 'Scenario', attribute_choice]
    # BOOM = reSampleData(df,GroupList = attributes)
    return attributes, attribute_choice#, BOOM

# *********** FILTERING  *********

def filter_parent(drivers, parent='Free Cash Flow'):
    """ Filters Parent Nodes """
    # print(f' AT {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} - Filtering Parent')
    drivers_parent = drivers.loc[drivers['Parent'] == parent].reset_index(drop=True)
    numerators = drivers_parent['Metric'].tolist()
    denominators = drivers_parent['Denominator'].tolist()
    return drivers_parent, numerators, denominators

def filter_drivers(drivers, df3, parent, startdate, enddate, caller='FHMS'):
    """ Calls f(x) to return lists for drivers, numerators and denominators"""
    # print(f'AT {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} Filtering Drivers')
    driver_parent, num, den = filter_parent(drivers, parent)
    # print(driver_parent, num, den)
    # ''' HAVE TO CHANGE HERE TO ALLOW TO FILTER HORIZONTALLY VERSES VERTICALLY'''

    if caller == 'FHMS':
        subsetdf = df3[df3['variable'].isin(num)] #filters DF by numerators
        # print(f'FHMS DATA from {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno}', subsetdf)
    else:
        # print(f'from filter {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno}')
        subsetdf =  df3.loc[startdate:enddate] #TODO #355 The user wants to filter the date on object creation this is the filter we will use in the object
        print('OTHER DATA')

    return subsetdf, driver_parent, num, den


    
