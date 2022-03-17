'''
This is the test suite for the cvai python methods in the transformation manager and filter manager
'''


import datetime

import pandas as pd
import pytest

import cvai.dictionary_testing_for_driverconfig as dc
import cvai.filter_manager as fm
import cvai.transformation_manager as tm
import unittest

class TestSetup:
    @pytest.mark.parametrize("filenamegetter, answer",[((True, 'Revenue', ['Scenario']),'file1'),((False, 'Revenue', ['Scenario', 'CAE']),'file6')], indirect=['filenamegetter'])
    def test_dictionary_for_passing_file_names_for_testdata(self,filenamegetter, answer):
        '''      '''
        # Setup
        # Exercise
        # Validate
        assert filenamegetter == answer
        #teardown

    def test_last_day_of_month(self):
        ''' Tests the Month date to be coverted to the last day of the month'''
        # setup
        desired_date1 = datetime.datetime(2020,2,29)
        desired_date2 = datetime.datetime(2021,2,28)
        desired_date3 = datetime.datetime(2021,3,31)
        desired_date4 = datetime.datetime(2021,4,30)

        # exercise
        calculated_date1 = tm.get_month_lastday('2020-02-02')
        calculated_date2 = tm.get_month_lastday('2021-02-02')
        calculated_date3 = tm.get_month_lastday('2021-03-02')
        calculated_date4 = tm.get_month_lastday('2021-04-02')

        # validate
        assert desired_date1 == calculated_date1
        assert desired_date2 == calculated_date2
        assert desired_date3 == calculated_date3
        assert desired_date4 == calculated_date4

        # teardown - none

    def test_initialize_dframes_in_trans_mgr(self):
        '''
        This tests the dataframe set up for the TM
        '''
        # Setup
        initialized_df = [pd.DataFrame() for i in range(6)]
        # Exercise
        calculated_df = tm.initialize_dframes()
        # Validate
        assert len(calculated_df)== len(initialized_df)
        # Teardown

    def test_make_dictionary_for_aggregations(self,drivers,desired_dictionary):
        '''
        This tests to see if the dictionary is created properly
        '''
        # Set'up
        desired_dictionary = {'Revenue': 'sum', 'Items': 'sum', 'SKU': 'nunique',
                                'Invoice': 'nunique', 'Product Line': 'nunique', 'Account': 'nunique',
                                'Rep': 'nunique', 'Manager': 'nunique', 'Team': 'nunique', 'Market': 'nunique'}
        # Exercise
        calculated_dictionary = dc.get_aggregation_dictionary(drivers)
        # Validate
        assert desired_dictionary == calculated_dictionary

        # Teardown

class TestsForFilterManager:

    def test_filtering_driver_parent_from_drivers(self,drivers, parent, expected_parent):
        '''
        This tests that the parent is being sent from the drivers
        file based on the input from the frontend
        '''
        # Setup - None (in the conftest)

        # Exercise
        filtered_parent_obj,_,_ = fm.filter_parent(drivers, parent)
        filtered_parent = pd.DataFrame(filtered_parent_obj)

        # Validate
        assert filtered_parent.Parent.all() == expected_parent.Parent.all()
        assert pd.testing.assert_frame_equal(filtered_parent, expected_parent) is None

        # Teardown

    def test_filtering_driver_parent_from_drivers_FHMS(self, FHMS_drivers, FHMS_parent, expected_parent_FHMS):
        '''
        This tests that the parent is being sent from the drivers
        file based on the input from the frontend
        '''
        # Setup - None (in the conftest)
        # Exercise
        filtered_parent_obj,_,_ = fm.filter_parent(FHMS_drivers, FHMS_parent)
        filtered_parent = pd.DataFrame(filtered_parent_obj)
        # filtered_parent.to_csv('filtered_parent.csv')
        # Validate
        assert filtered_parent.Parent.all() == expected_parent_FHMS.Parent.all()
        assert pd.testing.assert_frame_equal(filtered_parent, expected_parent_FHMS, check_dtype=False) is None

    def test_attribute_selection(self):
        # Setup
        attribs_none = None
        attribute_choice = 'TEST ATTRIBUTE'
        expected_attributes_none= ['variable', 'Scenario']
        expected_attributes = ['variable', 'Scenario', attribute_choice]
        dframe = []

        # Exercise
        calculated_attributes_none, attribs = fm.chose_details(dframe,attribs_none)
        calculated_attributes, attribs = fm.chose_details(dframe,attribute_choice)

        # Validate
        assert calculated_attributes_none == expected_attributes_none
        assert calculated_attributes == expected_attributes

        # Teardown

# @pytest.mark.parametrize('file_filtered_raw')
# class TestsForTransformationManager:
    ''' '''
@pytest.mark.parametrize("filegetter2", ["Filter SKU, ScenarioCAE","Filter Revenue, ScenarioCAE","Filter SKU, Scenario","Filter Revenue, Scenario"], indirect=True) 
def test_resampling_filter(expected_df_full_for_aug_sep_2020, filegetter2):
    '''      '''
    # Setup
    group_choice = filegetter2.get('group_sel')
    numers_choice = filegetter2.get('numers_sel')
    numers = [numers_choice]
    expected_df = pd.read_csv(filegetter2.get('file_loc'), parse_dates=True, index_col='Date')
    # Exercise
    calculated_resample_filter = tm.filter_for_resampling(expected_df_full_for_aug_sep_2020, numers, group_choice)
    # calculated_resample_filter.to_csv(r'./cvai/data/testsets/test_resampling_filter.csv', mode='a')
    # Validate
    assert pd.testing.assert_frame_equal(calculated_resample_filter,expected_df) is None
    # Teardown

@pytest.mark.parametrize("filegetter2", ["Revenue, Scenario, YTD", "Revenue, Scenario","SKU, Scenario", "SKU, Scenario, YTD","Revenue, ScenarioCAE, YTD", "Revenue, ScenarioCAE", "SKU, ScenarioCAE, YTD", "SKU, ScenarioCAE"], indirect=True)
def test_resample_data_for_TM(filegetter2, enddate, startdate, expected_df_full_for_aug_sep_2020):
    '''
    This is a test to check the integrity of the resample method     
    '''
    # Setup
    period = "MS"
    ytd_choice = filegetter2.get('ytd_sel')
    group_choice = filegetter2.get('group_sel')
    numers_choice = filegetter2.get('numers_sel')
    aggra = 'sum' if numers_choice == 'Revenue' else 'nunique'
    expected_resample = pd.read_csv(filegetter2.get('file_loc'), parse_dates=True, index_col='Date')
    
    # Exercise
    calculated_resample = tm.resample_data(expected_df_full_for_aug_sep_2020,numers_choice, group_choice, period, aggra, startdate, enddate, ytd_choice)
    # calculated_resample.to_csv(r'./cvai/test_resample_data_for_TM2.csv', mode='a')
    # Validate
    assert pd.testing.assert_frame_equal(calculated_resample,expected_resample, check_dtype=False) is None
    
    # Teardown

@pytest.mark.parametrize("filegetter2", ["Revenue, Scenario, YTD", "Revenue, Scenario","SKU, Scenario", "SKU, Scenario, YTD","Revenue, ScenarioCAE, YTD", "Revenue, ScenarioCAE", "SKU, ScenarioCAE, YTD", "SKU, ScenarioCAE"], indirect=True)
def test_aggregate_transaction_data(enddate, startdate, expected_df_full_for_aug_sep_2020, filegetter2):
    '''This test checks the aggregation of transaction data in the "aggregate_transaction_data" method.  It uses
    indirect parametrized fixtures to cycle through YTD, Attributes, and Aggregation.
    '''
    # Setup
    period = "MS"
    ytd_choice = filegetter2.get('ytd_sel')
    group_choice = filegetter2.get('group_sel')
    numers_choice = filegetter2.get('numers_sel')
    aggra = 'sum' if numers_choice == 'Revenue' else 'nunique'
    expected_df = pd.read_csv(filegetter2.get('file_loc'), parse_dates=True, index_col='Date')
    expected_df = expected_df[expected_df.Scenario =="ACTUALS"]
    if not ytd_choice:
        expected_df= expected_df.groupby(group_choice)[numers_choice].resample(period).agg(sum).reset_index(level=group_choice)
    # Exercise
    calculated_aggregated_data = tm.aggregate_actuals_data(expected_df_full_for_aug_sep_2020, group_choice, numers_choice, period, aggra, ytd_choice, enddate)
    # calculated_aggregated_data.to_csv(r'./cvai/data/expected_monthly_Revenue_scenarioCAE.csv')
    # Validate
    pd.testing.assert_frame_equal(calculated_aggregated_data, expected_df)
    # Teardown
@pytest.mark.parametrize("filegetter2", ["Revenue, Scenario, YTD", "Revenue, Scenario","SKU, Scenario", "SKU, Scenario, YTD","Revenue, ScenarioCAE, YTD", "Revenue, ScenarioCAE", "SKU, ScenarioCAE, YTD", "SKU, ScenarioCAE"], indirect=True)
def test_aggregate_plan_data(enddate, startdate, expected_df_full_for_aug_sep_2020, filegetter2):
    ''' 
    This test checks the aggregation of plan data in the "aggregate_plan_data" method.  It uses 
    indirect parametrized fixtures to cycle through YTD, Attributes, and Aggregation.     
    '''
    # Setup
    period = "MS"
    ytd_choice= filegetter2.get('ytd_sel')
    group_choice = filegetter2.get('group_sel')
    numers_choice = filegetter2.get('numers_sel')
    expected_df = pd.read_csv(filegetter2.get('file_loc'), parse_dates=True, index_col='Date').astype(float,errors='ignore')
    expected_df = expected_df[expected_df.Scenario =="PLAN"]
    if not ytd_choice:
        expected_df = expected_df if expected_df.empty else expected_df.groupby(group_choice)[numers_choice].resample(period).agg('sum').reset_index(level=group_choice)
    # Exercise
    calculated_plan_data = tm.aggregate_plan_data(expected_df_full_for_aug_sep_2020, group_choice, numers_choice, period, ytd_choice, startdate, enddate)
    # calculated_plan_data.to_csv(r'./cvai/data/RESULTS.csv')
    # Validate
    assert pd.testing.assert_frame_equal(calculated_plan_data,expected_df, check_dtype=False) is None
    # Teardown

def test_filtering_driver_numerators_and_denominators_from_parent_filtered_dataframe(drivers, parent, startdate, demo_data, enddate, expected_nums, expected_dens, expected_df_full_for_aug_sep_2020):
    '''
    This test checks the numerators, denominators, and the Dataframes are pulling the correct values for non- FHMS data.  
    This data works with the following fixture setting's:
   ' startdate = 2020-08-01, enddate= 2020-09-30, parent = 'Revenue' and the files in ./cvai/data 
    for  drivers, demo data, nums, dens, df as csv files.
    '''
    # Setup
    caller = "OTHER"
    # Exercise
    calculated_df, _, calculated_nums, calculated_dens = fm.filter_drivers(drivers, demo_data,parent, startdate, enddate, caller)
    calculated_num_df = pd.DataFrame(calculated_nums, columns=['Metric'])
    calculated_den_df = pd.DataFrame(calculated_dens, columns=['Denominator'])
    # print(f'{calculated_den_df =},{calculated_num_df=}, {calculated_df=}')
    # Validate
    assert pd.testing.assert_frame_equal(calculated_num_df,expected_nums) is None
    assert pd.testing.assert_frame_equal(calculated_den_df,expected_dens) is None
    pd.testing.assert_frame_equal(calculated_df, expected_df_full_for_aug_sep_2020,check_dtype=False)
    # Teardown  

@pytest.mark.parametrize("filegetter2", ["Drivers, Revenue, Scenario, YTD", "Drivers, Revenue, Scenario","Drivers, SKU, Scenario", "Drivers, SKU, Scenario, YTD","Drivers, Revenue, ScenarioCAE, YTD", "Drivers, Revenue, ScenarioCAE", "Drivers, SKU, ScenarioCAE, YTD", "Drivers, SKU, ScenarioCAE"], indirect=True)
def test_resample_data_for_alt_create_drivers(filegetter2, enddate, startdate, expected_df_full_for_aug_sep_2020,expected_parent, expected_nums, expected_dens):
    '''
    This is a test to check the integrity of the resample method     
    '''
    # Setup
    period = "MS"
    ytd_choice = filegetter2.get('ytd_sel')
    group_choice = filegetter2.get('group_sel')
    numers_choice = filegetter2.get('numers_sel')
    aggra = 'sum' if numers_choice == 'Revenue' else 'nunique'
    expected_resample = pd.read_csv(filegetter2.get('file_loc'), parse_dates=True, index_col='Date')
    
    # Exercise
    calculated_resample = tm.alt_create_drivers(expected_df_full_for_aug_sep_2020, expected_parent, expected_nums.Metric.unique().tolist(), expected_dens.Denominator.unique().tolist(),'MS', group_choice, startdate, enddate, ytd_choice)
    # calculated_resample.to_csv(r'./cvai/data/testsets/Drivers.csv', mode='a')
    # Validate
    assert pd.testing.assert_frame_equal(calculated_resample,expected_resample, check_dtype=False) is None


@pytest.mark.parametrize("filegetter2", ["Drive_x2_input"], indirect=True)
def test_splitting_dataframes(filegetter2,drivex):
    '''
    This is a test to check the integrity of the resample method     
    '''
    # Setup
    period = "MS"
    ytd_choice = filegetter2.get('ytd_sel')
    group_choice = filegetter2.get('group_sel')
    numers_choice = filegetter2.get('numers_sel')
    aggra = 'sum' if numers_choice == 'Revenue' else 'nunique'
    expected_driver = pd.read_csv(filegetter2.get('file_loc'), parse_dates=True, index_col='Date')
    
    # Exercise
    calculated_drivex, calculated_num, calculated_den = tm.split_drive_x2(drivex)
    # calculated_drivex.to_csv(r'./cvai/data/testsets/Drivex.csv')
    # calculated_num.to_csv(r'./cvai/data/testsets/Drivex_num.csv')
    # calculated_den.to_csv(r'./cvai/data/testsets/Drivex_den.csv')
    # Validate
    assert pd.testing.assert_frame_equal(calculated_drivex, expected_driver, check_dtype=False) is None

@pytest.mark.parametrize("filegetter2", ["Create_driver_input"], indirect=True)
def test_create_drivers(filegetter2,drivers, startdate, enddate,demo_data,parent):
    '''
    This is a test to check the integrity of the resample method     
    '''
    # Setup
    period = "MS"
    ytd_choice = filegetter2.get('ytd_sel')
    group_choice = filegetter2.get('group_sel')
    numers_choice = filegetter2.get('numers_sel')
    aggra = 'sum' if numers_choice == 'Revenue' else 'nunique'
    expected_driver = pd.read_csv(filegetter2.get('file_loc'), parse_dates=True, index_col='Date')
    
    # Exercise
    calculated_drivex, calculated_num, calculated_den = tm.create_drivers(demo_data, drivers, parent, period, group_choice,startdate, enddate, ytd_choice, caller='Other')
    # calculated_drivex.to_csv(r'./cvai/data/testsets/Driver_x.csv')
    # calculated_num.to_csv(r'./cvai/data/testsets/Drive_x_num.csv')
    # calculated_den.to_csv(r'./cvai/data/testsets/Drive_x_den.csv')
    # Validate
    assert pd.testing.assert_frame_equal(calculated_drivex, expected_driver, check_dtype=False) is None


 