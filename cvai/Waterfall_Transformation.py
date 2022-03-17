"""
This is how we will perform the waterfall transformation


Created on Tue Jul  7 20:47:49 2020

@author: michaelprinci
"""
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

# Zach Comment

import numpy as np
import pandas as pd

from charts import utils

import inspect

def get_month_lastday(aaa):
    return dt.strptime(aaa,'%Y-%m-%d') + relativedelta(day=31)  # End-of-month


def FilterSOCdates(DriversFile, start, end, pva = False):
    """ This is a Filter for Isolating single dates for a waterfall chart"""
    # TODO: [CAM-39] Consider how we will pass the initial and ending values into the waterfall for use in Hovers
    # print(f'into {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno}:\n',DriversFile, DriversFile.columns,start,end)
    # DriversFile.to_csv(r'./cvai/data/testsets/df_into_fsoc')
    startend = get_month_lastday(start).replace(day=1)
    endend = dt.strftime(get_month_lastday(end),"%Y-%m-%d")
    endstart= dt.strftime(get_month_lastday(end).replace(day=1),"%Y-%m-%d")
    target_scenario = 'BASELINE' if 'ACTUALS' not in DriversFile.Scenario.unique() else 'ACTUALS';# print(f'{target_scenario=}')

    if not pva: #

        namecol = 'Scenario'
        colfilter = DriversFile.Scenario.unique()[0] #replace with a dynamic connection to the front end
        # print(f'at {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno}', colfilter,DriversFile[DriversFile[namecol]==target_scenario])
        DriversFile = DriversFile[DriversFile[namecol]==target_scenario]
        # print(f"in {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno}:", DriversFile) 
        # print(f'Dates  {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno}:',start, startend, end, endend, endstart)
        c = DriversFile.loc[start]; print('c notpva here in WFT36:',c,pva)
        d = DriversFile.loc[endstart];print('d notpva here in WFT37:',d,pva)
        # '''
        # print(f'c in {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno}:\n',c,'d in WFT39:\n',d, colfilter)
        DriversSorted = c.append(d)


        # print(f" at {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno}: out of pva fsoc",DriversSorted)
        # DriversSorted.to_csv(r'./cvai/data/testsets/FilteredforWF_pva.csv')


        return DriversSorted
        # '''
    if pva:
        namecol = 'Date'
        colfilter = dt.strftime(get_month_lastday(end).replace(day=1),"%Y-%m-%d")
        DriversFile = DriversFile.reset_index(col_level = 0).rename(columns={'index':'Date'})

        print(f"*******in PVA at {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno}:\n:", DriversFile,pva)
        print(DriversFile['Scenario'].unique(), colfilter)
        DriversFile = DriversFile[DriversFile[namecol]==colfilter]
        print(DriversFile['Scenario'].unique())
        # print(f'at {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno}:Scenarios are ', DriversFile['Scenario'].unique()[0]," and ", DriversFile['Scenario'].unique()[1])
        c = DriversFile[DriversFile['Scenario'] == target_scenario]
        d = DriversFile[DriversFile.Scenario == 'PLAN'] #TODO #250 Adjust the hardcoded variables to make this dynamic
    
        DriversSorted = c.append(d)
        DriversSorted = DriversSorted.set_index(['Scenario'])

        DriversSorted.to_csv('FilteredforWF_notpva_inWFT63.csv')

        print("out of NOT pva fsoc",DriversSorted) 
        #DriversSorted.to_csv('FilteredforWF_notpva.csv')


        return DriversSorted
    

def Source_of_Change(a,b):
    """ Creates function to transform the start and end values to the Source of change values """
    np.seterr(divide='ignore', invalid='ignore')
    # Step 1  _THIS IS WHERE IT BREAKS - A SHOULD BE AN ARRAY of the START VALUES
    A = a
    # print(A)
    # print(a)
    # Step 2
    B = b
    # Step 3
    C = B-A
    # Step 4
    D = np.sign(A)*C/A
    y = np.size(A) # THIS SHOULD EQUAL THE NUMBER OF DRIVERS
    COLUMN = 2**np.arange(0,y).reshape(1,y) #develop the column values
    # print("COL = ",COLUMN)
    ROW = np.arange(2**y).reshape(2**y,1) # develop the row values
    E = np.remainder((ROW//COLUMN),2)  #creating the binary array for toggling changes
    F = (E == 0).astype(float) #creating the binary array for toggling start values (mirror of E)
    # Step 5
    DIFF = E * C

    # Step 6
    START = F * A
    # Step 7
    COMBINED = DIFF + START
    # Step 8   s
    DELTAS = np.prod(COMBINED, axis =1).reshape(2**y,1)
    # Step 9
    DENOM = np.nan_to_num(((E*np.absolute(D))@np.ones(y))).reshape(2**y,1)
    # Step 10
    ALLOCATED_DELTAS = (E*np.absolute(D))/(DENOM)*DELTAS
    ALLOCATED_DELTAS = np.nan_to_num(ALLOCATED_DELTAS)
    # Step 11
    ANSWER = np.ones(2**y)@ALLOCATED_DELTAS
    np.set_printoptions(precision=3,suppress=True)
    return ANSWER

def get_waterfall(DriversSorted, drivers, is_sorted=False, parent_variable=None, pva= False):
    """ Creates Waterfall chart for the answers from Source of Change"""
    # Step 3: Pivot

    # print("&&&#####$$$$$$$", DriversSorted)
    # DriversSorted.to_csv(r"./cvai/data/testsets/driversorted_from_wtget_wf.csv")
    DriversSorted = DriversSorted if 'value' in DriversSorted.columns else DriversSorted.rename(columns={'Driver Value':'value'})
    dfp = DriversSorted.pivot(columns='Driver', values='value') #NEEDS TO CHANGE TO DRIVER VALUE COLUMN
    # dfp.to_csv(r'./cvai/data/testsets/dfp.csv', mode='a')
    print("DFP in WFT112:\n",dfp) #TODO This might be a good place to get the starting and ending values for use in the hovers in the waterfall chart
    
    array = dfp.to_numpy() # TODO: Fix Array Variable Name
    # print("ARRAY in WTF115:\n\n",array)
    # np.savetxt("foo.csv", array, delimiter=",")


    startpoint = array[1] if pva else array[0] # THIS HAS TO BE ADJUSTED AS IT CONTROLS THE ORDER DESPITE ORDER PASSED
    endpoint = array[0] if pva else array[1]
    startlabel = dt.strftime(dfp.index[0],"%b, %Y")  if isinstance(dfp.index, pd.DatetimeIndex) else dfp.index[1] 
    endlabel = dt.strftime(dfp.index[1],"%b, %Y") if isinstance(dfp.index, pd.DatetimeIndex) else dfp.index[0]

    try:
        startlabel = dt.strftime(dt.strptime(dfp.index[0],"%Y-%m-%d"),"%b %Y")
    except:
        startlabel = startlabel

    try:
        endlabel = dt.strftime(dt.strptime(dfp.index[1],"%Y-%m-%d"),"%b %Y")
    except:
        endlabel = endlabel

    # print(startlabel, endlabel)
    # print('\n*********',startpoint,'************')
    startvalue = startpoint.prod()
    # print(startvalue)

    # Imports dictionary and creates list of label names
    label_dict = utils.get_label_dict(drivers)
    label_names = []
    for i in dfp.columns:
        label_names.append(label_dict.get(i))

    #step 5: Pass and Return from function
    ans = Source_of_Change(startpoint,endpoint)
    plotdf = pd.DataFrame(ans, columns = [("DriverValue")])

    labelingDF =dfp.reset_index()
    Labels = label_names ## TODO: The labeling should happen here (label_names replaces dfp.columns)
    Labels = pd.DataFrame(Labels, columns =["Driver"]) # TODO: [CAM-46] Possible place to substitute labels for Waterfalls

    new = Labels.join(plotdf)
    # print(new)
    newsorted = new

    # Step 7: Sort by Value CAN BE OPTIONAL for non-arching plots

    if is_sorted:  # TODO: We should consider how we will sort by order - not aphabetically

        newsorted = new.sort_values(by = ['DriverValue'], ascending = False)
        newsorted = newsorted.reset_index(drop = True)

    # Step 8: Adds new row for start point and then re-indexes
    
    newsorted.loc[-1] = [(startlabel), startvalue]  # adding a row
    newsorted.index = newsorted.index + 1  # shifting index
    newsorted = newsorted.sort_index()  # sorting by index

    # Step 9: Creates Blank Series
    invis = newsorted.DriverValue.cumsum().shift(1).fillna(0)
    newsorted["invisible"]= invis

    # Step 10: Get the net total number for the final element in the waterfall and add to dataframe
    total = newsorted.sum().DriverValue
    items = newsorted.index.size
    newsorted.loc[items]= [str(endlabel),total,0]

    # Step 11: Combine into original dataset, filter and plot
    newsorted.loc[:,'Scenario'] = ("Change Values")  # adding the label for scenario 
    newsorted['Date']= max(DriversSorted['Date']) if pva else max(DriversSorted.index)#dt.now().strftime('%m/%d/%Y')# adding the current date to Date 
    ''' These might not be needed'''
    newsorted = newsorted[['Driver','Scenario','DriverValue','invisible']]
    datasetnew = newsorted

    # Step 12 Add Color for Bars to dataframe
    datasetnew.loc[datasetnew['DriverValue']  < 0.0, 'BarColor'] = 'Red'
    datasetnew.loc[datasetnew['DriverValue']  > 0.0, 'BarColor'] = 'Green'
    datasetnew.loc[datasetnew['DriverValue'] == 0, 'BarColor'] ="#b4b2b3"
    datasetnew.loc[datasetnew.Driver == (startlabel), 'BarColor']= '#729BC7'
    datasetnew.loc[datasetnew.Driver == (endlabel), 'BarColor']= '#729BC7'

    # Setp 13 add measures and Parent
    datasetnew['Measure'] = 'relative'
    datasetnew.loc[datasetnew.Driver == (startlabel), 'Measure']= 'absolute'
    datasetnew.loc[datasetnew.Driver == (endlabel), 'Measure']= 'absolute'
    parent = DriversSorted['Parent'].iloc[0]
    # print(f'{datasetnew=}')
    return datasetnew
