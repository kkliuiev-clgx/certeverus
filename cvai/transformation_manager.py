
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is how we will filter for the Source of Change for the Multifactor Drivers


Created on Sat Jul  4 12:25:10 2020

@author: michaelprinci
"""
from cvai.gdsingestion import count_unique_actuals
import pdb
import pandas as pd
from datetime import datetime as dt
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from dateutil.relativedelta import relativedelta
import inspect
try:
    from cvai import filter_manager as fmp
    from cvai import dictionary_testing_for_driverconfig as dc
except ImportError:
    import filter_manager as fmp
    import dictionary_testing_for_driverconfig as dc


def initialize_dframes():
    """ initialize DataFrames """
    print(
        f'Initializing Drivers Data Frames at {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno}')
    df_names = ['num_x', 'NumX2', 'DenX', 'DenX2', 'DriveX', 'DriveX2']
    num_x, num_x2, den_x, den_x2, drive_x, drive_x2 = [
        pd.DataFrame() for df in df_names]
    return num_x, num_x2, den_x, den_x2, drive_x, drive_x2


# TODO #262 This has to accommodate the time period, parameters, and aggregation
def get_ytd(dframe, startex, endex, group_list, aggra='sum', numers=None):
    # print(f'ENTERED YTD:\n at {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno}',dframe)
    endend = dt.strftime(get_month_lastday(endex), "%Y-%m-%d")
    # print(f'at {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} AGGRA:',aggra,endex, endend, group_list, numers)
    # dframe = dframe.drop(columns='index')
    # print(dframe[numers[0]])

    if numers is None:
        print('Passed numers test')
        dframe_ytd = dframe.loc[startex:endend].groupby(
            group_list).agg(aggra).reset_index()
    else:
        if is_numeric_dtype(dframe[numers[0]]):
            # print(f'numeric: {numers =},{aggra =}, {group_list=}')
            # TODO #260 The user should be able to use this for aggregate and detialed attributes
            dframe_ytd = dframe.loc[startex:endend].groupby(
                group_list).agg(aggra).reset_index()
        else:
            # print(f'STRING: {numers =},{aggra =}, {group_list=}')
            # filter by date, then grouplist and treat differently
            dframe_ytd = dframe.loc[startex:endend].groupby(
                group_list).nunique()
            # print(f'at {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} Nunique dframe:\n',dframe_ytd)
            dframe_ytd = dframe_ytd.drop(columns=group_list, axis=1)
            dframe_ytd['Scenario'] = dframe['Scenario'].unique()
            # print(f'{inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} {dframe_ytd=}')
        # pdb.set_trace()

    # aggra = 'sum'
    return dframe_ytd, aggra


def rebuild_ytd(dframe_ytd, endex):
    endex = dt.strftime(get_month_lastday(endex).replace(day=1), "%Y-%m-%d")
    dframe_ytd['Date'] = endex
    dframe_ytd['Date'] = pd.to_datetime(dframe_ytd['Date'], errors='coerce')
    # print(f'{dframe_ytd =}')
    dframe_ytd = dframe_ytd.reset_index(drop=True)
    dframe_ytd = dframe_ytd.set_index('Date', drop=True)
    dframe_ytd = dframe_ytd.drop(
        columns='index') if 'index' in dframe_ytd.columns else dframe_ytd
    # print(f'{dframe_ytd=}\n\nOUT\n\n\n\n')
    return dframe_ytd


def get_month_lastday(target_date):
    # End-of-month
    return dt.strptime(target_date, '%Y-%m-%d') + relativedelta(day=31)


'''
******************
OLD DRIVER CALCS
******************

1. filter Drivers for Parent and Driver 
2. calcs ***YTD*** if ytd True
3. chose details
4. Resample
5. build drivers
5a calc values
'''


# todo #275 Split Transformation Manager for FHMS versus Non FHMS
def re_sample_data(dframe, group_list=['variable', 'Scenario'], period='MS'):
    """ Gets user input for the resampling of data before plotting and can pass an optional
     list of parameters to groupby and optional Period, by GroupList = None
    """
    print("Resampling Data in resampler for", group_list, " and ", period)

    # print(dframe)
    merge_group = ['Date']

    merge_group = merge_group + group_list
    print("from resample\n", dframe)
    print(merge_group, group_list)
    # sets the
    # samples for monthly sums
    df_monthly = (dframe.groupby(group_list).resample(
        period).sum()).reset_index()
    df_daily = (dframe.groupby(group_list).resample('D').sum().reset_index(
        drop=False))  # samples daily to get the last day values
    df_daily = df_daily.set_index('Date')  # resets to date index
    df_last = df_daily.groupby(group_list).resample(period).last().reset_index(
        level=group_list, drop=True)  # gets last day values
    # changes the value column title to last in preparation for the merge
    df_last = df_last.rename(columns={'value': 'last'})
    df_unique = pd.DataFrame()  # dframe.groupby(group_list).resample(period).nunique()[
    # 'Location'].reset_index()  # gets unique values for an attribute
    # Build reSampled dataframe
    df_new = df_monthly  # .merge(df_unique, how='left', on=merge_group)
    # dfnew.to_csv('Merged with Nunique1.csv')
    df_new1 = df_new.merge(df_last, how='left', on=merge_group)
    # df_new1.to_csv('Merged with nUnique.csv')
    print('****** DONE FROM RESAMPLING ******')
    # print(df_new1[group_list[-1]].unique())
    return df_new1


def CreateDrivers(drivers, df3, parent, resample_period, attribs, startdate, enddate, ytd=False):
    """ Filter Dataframe and create Drivers"""
    subsetdf, driver_parent, num, den = fmp.filter_drivers(
        drivers, df3, parent, startdate, enddate)  # parent & drivers

    # subsetdf.to_csv(r"./catch/pre-ytd.csv")

    group_list = []

    group_list = ['variable', 'Scenario'] if attribs is None else [
        'variable', 'Scenario', attribs]
    print(group_list, attribs)

    print(" at line121:", subsetdf, group_list)
    if ytd:
        print('$$$$$$$$$     YTD  $$$$$$$$$$')
        subsetdf = get_ytd(subsetdf, startdate, enddate,
                           group_list, aggra='sum', numers=None, )
        print("at line 125:", subsetdf)
    subsetdf = subsetdf[0] if isinstance(subsetdf, tuple) else subsetdf

    # subsetdf.to_csv(r'./catch/post_ytd.csv')

    # gets attributes -  Can this be pushed into params for SQL?
    attributes, choice = fmp.chose_details(subsetdf, attribs)
    # should be replaced with call to new resampler
    resampled_df = re_sample_data(
        subsetdf, group_list=attributes, period=resample_period)

    # ,resampled_df.columns,attributes)
    print("********* IN CD fx Resampled DF *********")
    # print('Creating Drivers for ', driver_parent)
    drive_x2, num_x2, den_x2 = build_drivers_dframes(
        driver_parent, num, den, attributes, choice, resampled_df)

    # drive_x2.to_csv('POST_DRIVER_CREATION.csv') # GETS JUST ONE DRIVER

    return drive_x2, num_x2, den_x2


def build_drivers_dframes(driver_parent, num, den, attributes, choice, resampled_df):
    """ Loop to populate numerator and denominators for calulating driver values from the  """
    num_x, num_x2, den_x, den_x2, drive_x, drive_x2 = initialize_dframes()
    print('DRIVER PARENT TM148:',
          driver_parent['Parent'][0], attributes[-1], num, den)
    for i in enumerate(driver_parent['Driver']):
        for pro in resampled_df[attributes[-1]].unique():
            print("TM151 pro:", pro)
            print(attributes, pro,
                  " in BDF in TM 152***************************************")
            print(resampled_df['Scenario'].unique(
            ), " in BDF TM153 **************************", driver_parent['Driver'][i[0]])
            driver_name = (driver_parent['Driver'][i[0]])
            # DriverName = (Num[i[0]]+"/"+ Den[i[0]]) # prints the driver
            # populates numerator
            num_x = calculate_value(resampled_df, num[i[0]])
            # populates denominator
            den_x = calculate_value(resampled_df, den[i[0]])
            print('TM 158 Calculating for BDF for ', i,)  # , num_x,den_x)png

            drive_x['value'] = num_x.value / \
                (1 if den_x.empty else den_x.value)  # populates the Driver
            drive_x['Driver'] = driver_name
            drive_x['Parent'] = driver_parent['Parent'][0]
            # print(drive_x, num_x.Scenario)
            drive_x = drive_x.reset_index(
                inplace=False, col_fill='Date').rename(columns={'index': 'Date'})
            # print(drive_x)
            num_x = num_x.reset_index(inplace=False, col_fill='Date').rename(
                columns={'index': 'Date'})
            drive_x['Scenario'] = num_x.Scenario
            drive_x = drive_x.set_index('Date')
            num_x = num_x.set_index('Date')

            if choice is not None:
                attrib = [col for col in num_x.columns if col ==
                          choice]  # Changed to solve issue in 169
                drive_x[attrib] = num_x[attrib]
                # den_x['Attribute'] = den_x[attrib]
                print("DENX from TM175:\n", den_x)

        num_x2 = num_x2.append(num_x, ignore_index=False)
        den_x2 = den_x2.append(den_x, ignore_index=False)
        drive_x2 = drive_x2.append(drive_x)
        num_x = pd.DataFrame()
        den_x = pd.DataFrame()
        drive_x = pd.DataFrame()
        # DriveX2.rename(columns ={'Attribute':Attrib})
    # print('Drivers Passed from BDF\n\n',DriveX2)
    pd.set_option('display.max_columns', None)
    print('DRIVEX in TM186:\n', drive_x2, drive_x2.columns, '\nNUMX in TM186:\n',
          num_x2, num_x2.columns, '\nDENX in TM186:\n', den_x2, den_x2.columns)
    return drive_x2, num_x2, den_x2


def calculate_value(dframe, position):
    """ THIS PASSES A DATAFRAME FOR EACH OF THE NUMERATORS AND DENOMINATORS"""
    # print('FROM CV: Calculating Values for', position)
    pos_value = dframe[dframe['variable'] == (position)]
    # print(pos_value)
    # Change the calc to create the array that comprises the column that is of interest

    # FHMS substitutions

    if pos_value['variable'].all() == 'Exam Rooms':
        pos_value['value'] = pos_value['last']
        # pos_value.to_csv('examroomchange.csv')
    # if pos_value['variable'].all() == 'Locations': #TODO #104 Clean LocNos
        # print('TM203:Pos value',pos_value)
        # pos_value['value'] = pos_value.apply(lambda x:x['Location'] if x['Scenario']=='ACTUALS' else x['last'],axis =1)
        # pos_value.to_csv('Locchange.csv')
    # End of FHMS substitutions

    pos_value = pos_value.replace(0, method='bfill').set_index('Date')
    return pos_value  # returns the value for either numerator and denominator


'''
*******************************
NEW RESAMPLING AND DRIVER CALCS 
*******************************

This should be brought into CreateDrivers() and pass additional parameters from the frontend
1. Filter DFs
2. create drivers and return Drive_X2
3. split df

'''


def create_drivers(dfc, drivers, driver_parent, resample_period, attributes, startdate, enddate, ytd, caller='Other'):
    # print(f"At {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} Drivers:",drivers)
    # FILTER DRIVERS
    dfc, driver_parent, num, den = fmp.filter_drivers(
        drivers, dfc, driver_parent, startdate, enddate, caller)
    # print(f"FROM {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno}:",driver_parent)#,"coluns:\n",dfc.columns,"\n attributes:",attributes)
    # CREATE DRIVER DF

    if any(x in attributes for x in drivers.Metric.to_list()):
        # print(f'PROBLEM: {attributes} is in {drivers.Metric.to_list()}')
        new_col = (attributes[-1])+"_resamp"
        # print(f'{new_col}')
        dfc[new_col] = dfc[attributes[-1]]
        attributes.pop(-1)
        attributes.append(str(new_col))
        # print(f'New {new_col} attributes {attributes} and DFC:\n {dfc}')
    else:
        print('NO PROBLEM')
        # print(f' NO PROBLEM: {attributes} and {drivers.Metric}.to_list()')

    drive_x2 = alt_create_drivers(
        dfc, driver_parent, num, den, resample_period, attributes, startdate, enddate, ytd)
    # SPLIT TO MATCH OLD PLOTTING (will refactor)
    drive_x2, num_x2, den_x2 = split_drive_x2(drive_x2)
    # print(f' At {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} DRIVEX2 = {drive_x2}')
    return drive_x2, num_x2, den_x2  # EVENTUALLY WE CAN RETURN ONLY THE drive_x2


def alt_create_drivers(dfc, driver_parent, num, den, resample_period='A', attributes=['Scenario'], startdate='2020-01-01', enddate='2020-08-01', ytd=None):
    # rm hard code scenario
    '''This method create driver dataframes for WIDE data '''
    # this will go over to replace the build driver df in TM

    # This block gets Atrributes and agg types for method -  will come from frontend and postgres?
    dict_test = dc.get_aggregation_dictionary(driver_parent)
    num_x, num_x2, den_x, den_x2, drive_x, drive_x2 = initialize_dframes()

    print(f'FROM {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} = {dict_test} and attributes in alt create: {attributes}')

    for i in enumerate(driver_parent['Driver']):
        # This block loops driver file
        # print(driver_parent, num[i[0]], den[i[0]],i)
        # make this a list to unpack?
        numerator, denominator = num[i[0]], den[i[0]]
        aggregate = (dict_test[numerator])  # loop through the list?
        aggregate_d = None if denominator == '1' else (dict_test[denominator])
        driver_name = (driver_parent['Driver'][i[0]])
        # print(f'At {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno}: {attributes=} {numerator=} {denominator=}')
        # Next line brings back NUMX or does this go to Calc?

        # RESAMPLING HERE --> set as a METHOD? COULD LOOP IF NUMERATOR AND DENOMINATOR ARE A LIST
        # print(f'At {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} FOR NUMERATOR for ', i[1],' - ',numerator )
        drive_x = resample_data(
            dfc, numerator, attributes, resample_period, aggregate, startdate, enddate, ytd=ytd)
        # print(f' at {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} FOR Denominator for {i[1]} - denominator and {attributes}' )
        den_x = 1 if denominator == '1' else resample_data(
            dfc, denominator, attributes, resample_period, aggregate_d, startdate, enddate, ytd=ytd)

        # print(f' At {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} INSIDE LOOP:\n\n',i, drive_x)
        # brings back DENOMX

        # REBUILDING THE DRIVER DATAFRAME AND CALC FOR DRIVER VAL
        drive_x['Numerator'] = numerator
        drive_x['Denom Value'] = 1 if denominator == '1' else (
            den_x[denominator])
        drive_x['Denom Value'] = drive_x['Denom Value'].apply(
            lambda x: float(x))
        drive_x['Denominator'] = denominator
        drive_x[numerator] = drive_x[numerator].apply(lambda x: float(x))
        drive_x['Driver'] = driver_name
        drive_x['Parent'] = driver_parent['Parent'][0]

        # CALC FOR DRIVER VALUE
        drive_x['Driver Value'] = (
            drive_x[numerator]/drive_x['Denom Value'])  # DRIVEX
        drive_x = drive_x.rename(columns={numerator: "Num Value"})

        # combine
        drive_x2 = drive_x2.append(drive_x)

        # print('DRIVEX@ =',drive_x2)

    return drive_x2


def filter_for_resampling(dfc, numers, group_list):
    # print(f' in {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} for resampling before {dfc=}') #filter the numerator or denom and attributes
    dfc = dfc.filter(items=group_list+numers)
    # print(f' in {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} for resampling after {dfc=}') #filter the numerator or denom and attributes
    return dfc


def get_plan_and_baseline(dfc, group_list, period, startdate, enddate, ytd, numers, aggra):
    dfcn_baseline = pd.DataFrame()
    dfcn_plan = pd.DataFrame()
    dfcn_control = pd.DataFrame()

    if "PLAN" in dfc.Scenario.unique():
        dfcn_plan = aggregate_plan_data(
            dfc, group_list, numers, period, ytd, startdate, enddate)

    if "BASELINE" in dfc.Scenario.unique():
        print("BASELINE Present")
        dfcn_baseline = aggregate_actuals_data(
            dfc, group_list, numers, period, aggra, ytd, enddate, 'BASELINE')

    if "CONTROL" in dfc.Scenario.unique():
        print("CONTROL Present")
        dfcn_control = aggregate_actuals_data(
            dfc, group_list, numers, period, aggra, ytd, enddate, 'CONTROL')

    return dfcn_plan, dfcn_baseline, dfcn_control


# need to run parameters through to check conditions
def aggregate_plan_data(dfc, group_list, numers, period, ytd, startdate, enddate):
    # print(f'PLAN EXISTS {numers =},{group_list=}, {dfc.Scenario.unique()=}')
    dfc1 = dfc[dfc['Scenario'] == 'PLAN']
    """     # try:
        #     dfc1 = dfc if dfc[numers].dtypes.all() == 'float64' else dfc.apply(pd.to_numeric,errors='coerce', axis=1)
        # except:
        #     dfc1 = dfc if dfc[numers].dtypes == 'float64' else dfc.apply(pd.to_numeric,errors='coerce', axis=1)
    """
    dfc1.loc[:, 'Scenario'] = 'PLAN'
    if not ytd:
        # print(f'{ytd=} in agg function2 at {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno}')
        try:
            # print(f'{dfc1=} , {dfc1.dtypes=}')
            dfcn2 = dfc1[dfc1['Scenario'] == 'PLAN'].groupby(
                group_list)[numers].resample(period).agg('sum')
            print("SUm line ran")
        except:
            dfcn2 = dfc1[dfc1['Scenario'] == 'PLAN'].groupby(group_list)[
                numers].agg('nunique')
        # dfcn2 = dfc.groupby(group_list.remove('Scenario'))[numers].resample(period).agg(sum)
        # print(f'{dfcn2=} INSIDE FUNCTION')
        # add a transactional and plan aggregation item in config
        dfcn2 = dfcn2 if dfcn2.empty else dfcn2.reset_index(level=group_list)
    else:
        # print(f'{ytd=} in agg function2')
        try:
            agga_here = 'sum' if dfc[numers].dtypes == 'float64' else 'mean'
        except:
            agga_here = 'sum' if dfc[numers].dtypes.all(
            ) == 'float64' else 'nunique'

        dfc1 = dfc1[dfc1['Scenario'] == 'PLAN'].astype(float, errors='ignore')
        dfcn2 = dfc1[dfc1['Scenario'] == 'PLAN'].groupby(
            group_list)[numers].agg(agga_here).reset_index(level=group_list)
        dfcn2 = rebuild_ytd(dfcn2, enddate)
        # dfcn2 = dfcn2 if dfcn2.index.dtype else
    # print(f'{dfcn2 = } FROM PLAN {ytd=}')
    newstring = group_list + [numers]
    dfcn2 = pd.DataFrame(columns=newstring, index=pd.to_datetime(
        [])).rename_axis('Date') if dfcn2.empty else dfcn2
    return dfcn2


def aggregate_actuals_data(dfc, group_list, numers, period, aggra, ytd, enddate, case="ACTUALS"):
    if not ytd:
        # print(f'{ytd =} in agg function1, {dfc=}')
        dfcn1 = dfc[dfc['Scenario'] == case].groupby(group_list)[numers].resample(
            period).agg(aggra).reset_index(level=group_list)
    else:
        dfcn1 = dfc[dfc['Scenario'] == case].groupby(
            group_list)[numers].agg(aggra).reset_index(level=group_list)
        dfcn1 = rebuild_ytd(dfcn1, enddate)

    return dfcn1

    """ # def check_and_call_ytd(ytd, dfc, startdate, enddate, group_list, aggra, numers):
    #     ''' Checks and calls ytd '''
    #     print("checking conditional")
    #     dfc, aggra = get_ytd(dfc, group_list, numers, period, aggra, ytd, enddate) if ytd else dfc, aggra
    #     return aggra, dfc 
    # """


def resample_data(dfc, numer, group_list, period, aggra, startdate, enddate, ytd=None):
    ''' THIS IS Where the REFACTOR Happens'''
    # Calcs for refactoring
    # print(f'into resample at {inspect.getframeinfo(inspect.currentframe()).function}, {inspect.getframeinfo(inspect.currentframe()).lineno}')
    dfcn_plan = pd.DataFrame()  # initializes an empty dataframe for plan
    numers = [numer]
    # filter the numerator or denom and attributes
    dfc = filter_for_resampling(dfc, numers, group_list)

    """     # print(f'FROM {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} \n Numers are: {numers=}, Grouplist is {group_list=}, {aggra=}, {ytd=} \n\n')
        # print(f'FROM {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} {dfc=} \n\n\n')
        # CONDITIONAL YTD
        # aggra, dfc = check_and_call_ytd(ytd, dfc, startdate, enddate, group_list, aggra, numers)
        
        # print(f'INTO RESAMPLE:, {aggra=}, {group_list=}, {period=}, {startdate=}, {enddate=}, {ytd=}')
        # print(f'DFC BEFORE RESAMPLE:, {dfc=}')
        
        # Build Resamples for calculating drivers

        # if not ytd:
        # print(f'SLIPSTREAM {ytd=}, {period=},{group_list =}')
    """
    dfcn_actuals = aggregate_actuals_data(
        dfc, group_list, numers, period, aggra, ytd, enddate)

    dfcn_plan, dfcn_baseline, dfcn_control = get_plan_and_baseline(
        dfc, group_list, period, startdate, enddate, ytd, numers, aggra)  # wh
    # dfcn_plan =  aggregate_actuals_data(dfc, group_list, numers, period, aggra, ytd, enddate, "PLAN")

    # print(f'AT {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} {dfcn_actuals=} ,\n {dfcn_plan=} Aggregated for {aggra=}')
    dfcn = dfcn_actuals if dfcn_plan.empty else dfcn_actuals.append(dfcn_plan)
    dfcn = dfcn if dfcn_baseline.empty else dfcn.append(dfcn_baseline)
    dfcn = dfcn if dfcn_control.empty else dfcn.append(dfcn_control)
    # print(f'{dfcn=} {dfcn_actuals=} \n FROM {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno}')
    dfcn[numer] = dfcn[numer].apply(lambda x: float(x))

    """     # print("DFCN3",f'{dfcn=})
        # dfcn = dfcn.reset_index(drop=False)
        # else:
            # print(f'Treelanding- {ytd =} {aggra =}')
            # dfcn = dfc[0].groupby(group_list)[numers].resample(period).agg(sum).reset_index() #PROBLEM

        # print(f'At {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} DFCN4:',dfcn)
        # dfcn = dfcn.set_index(['Date']) #PROBLEM TO AVOID
        # print(f'At {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} DFCN after groupby:\n',dfcn, '\n\n\n\n')
    """

    dfcn = filter_for_resampling(dfcn, numers, group_list)  # for DriveX
    # print(f'At {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno}: FINAL TO CREATE DRIVER\n {dfcn} \n###############\n')
    return dfcn


def split_drive_x2(drive_x2):
    ''' 
    This allows for splitting to accommodate the current plotting treatments with 3 dataFrames 
    '''
    num_x2 = drive_x2.drop(
        ['Denom Value', 'Denominator', 'Driver Value', 'Driver'], axis=1)
    num_x2 = num_x2.rename(
        columns={'Num Value': 'value', 'Numerator': 'variable'})
    den_x2 = drive_x2.drop(
        ['Num Value', 'Numerator', 'Driver Value', 'Driver'], axis=1)
    den_x2 = den_x2.rename(
        columns={'Denom Value': 'value', 'Denominator': 'variable'})
    drive_x2 = drive_x2.rename(columns={'Driver Value': 'value'})

    return drive_x2, num_x2, den_x2

# TODO #264 Consider Unpack the params in the transformation manager - will this give use flexibility for other products (e.g. SVA and pla
