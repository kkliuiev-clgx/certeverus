'''
This is the test suite for the cvai python methods in the trnasformation manager and filter manager
'''


# import datetime

import pickle
import unittest
import json
# import plotly
import os
import platform

import pandas as pd
import pytest

import cvai.PlotSingleFactor as psf
# import cvai.filter_manager as fm
# import cvai.transformation_manager as tm
import cvai.singleFactorTransformation as sft
import cvai.PlotIsoquant as pi
import cvai.sparklineTransformation as slt
import cvai.plotNodeMap as pnm
import cvai.PlotWaterfall as pwf
import cvai.PlotCoverSheet as pcs
import cvai.Waterfall_Transformation as wft


def test_singlefactor(request, drivers):
    '''   This method tests the SingleFactor Transformation  '''
    # Setup
    df_input = pd.read_csv(r'./cvai/data/Drivers_Revenue_Scenario.csv', parse_dates=True, index_col='Date')
    expected_drivers = pd.read_csv(r'./cvai/data/expected_posted_drivers.csv', parse_dates=True, index_col='Date')

    # Exercise
    _, target_driver, target_num, target_denom, posted_drivers, posted_num, posted_denom = sft.get_SingleFactor(df_input, df_input, df_input, drivers, driver_choice='Revenue/Items', attributes=None)
    # Validate
    assert pd.testing.assert_frame_equal(posted_drivers, expected_drivers, check_dtype=False) is None
    # Teardown
    request.config.cache.set("driver", target_driver)
    request.config.cache.set("target_driver", target_driver)
    request.config.cache.set("target_num", target_num)
    request.config.cache.set("target_denom", target_denom)
    request.config.cache.set("posted_drivers", posted_drivers.to_json(orient='table'))
    request.config.cache.set("posted_nums", posted_num.to_json(orient='table'))
    request.config.cache.set("posted_denoms", posted_denom.to_json(orient='table'))


def test_plotSinglefactor(request):
    '''   This method tests the SingleFactor Plotting and compares a figure dictionary to the calculated figure dictionary   '''
    # Setup
    with open(r"./cvai/data/testsets/singlefactor.pkl", 'rb') as expected:
        expected_chart = pickle.load(expected)
    driver_parent = request.config.cache.get("driver", None)
    target_driver = request.config.cache.get("target_driver", None)
    target_num = request.config.cache.get("target_num", None)
    target_denom = request.config.cache.get("target_denom", None)
    posted_drivers = pd.read_json(request.config.cache.get("posted_drivers", None), orient='table').set_index('Date')
    posted_num = pd.read_json(request.config.cache.get("posted_nums", None), orient='table').set_index('Date')
    posted_denom = pd.read_json(request.config.cache.get("posted_denoms", None), orient='table').set_index('Date')
    # Exercise
    calculated_chart = psf.plotSingleFactor(driver_parent, target_driver, target_num, target_denom, posted_drivers, posted_num, posted_denom)

    # Validate
    assert calculated_chart == expected_chart
    # Teardown


def test_PlotIsoquant(request):
    ''' This method tests the plot isoquant and compares the figures produced  '''
    # Setup
    with open(r"./cvai/data/testsets/isoquant.pickle", "rb") as infile:
        expected_chart = pickle.load(infile)
    driver_parent = request.config.cache.get("driver", None)
    target_driver = request.config.cache.get("target_driver", None)
    target_num = request.config.cache.get("target_num", None)
    target_denom = request.config.cache.get("target_denom", None)
    posted_drivers = pd.read_json(request.config.cache.get("posted_drivers", None), orient='table').set_index('Date')
    posted_num = pd.read_json(request.config.cache.get("posted_nums", None), orient='table').set_index('Date')
    posted_denom = pd.read_json(request.config.cache.get("posted_denoms", None), orient='table').set_index('Date')
    # Exercise
    calculated_chart = pi.plotisoquant(driver_parent, target_driver,target_num,target_denom, posted_drivers, posted_num, posted_denom, attribs=None, ytd=False)
    # with open(r"./cvai/data/testsets/isoquant.pickle", "wb") as outfile:
    #      pickle.dump(calculated_chart, outfile)
    # Validate
    assert calculated_chart == expected_chart
    # Teardown


def test_sparkline_transformation(drivers):
    '''   This method tests the sparkline figures   '''
    # Setup
    df_input = pd.read_csv(r'./cvai/data/Drivers_Revenue_Scenario.csv', parse_dates=True, index_col='Date')
    filename = r"./cvai/data/testsets/sparkline_windows.pickle" if platform.system() == 'Windows' else r"./cvai/data/testsets/sparkline.pickle"
    
    with open(filename, "rb") as infile:
        expected_chart = pickle.load(infile)
    # with open(r"./cvai/data/testsets/sparkline.json", "r") as infile:
    #     expected_chart = json.load(infile)
    # Exercise
    calculated_chart = slt.Sparkline(df_input)
    # with open(r"./cvai/data/testsets/sparkline_windows.pickle", "wb") as outfile:
    #     pickle.dump(calculated_chart, outfile)
    # with open(r"./cvai/data/testsets/sparkline.json", "w") as outfile:
    #     jfig =json.dumps(calculated_chart)
    #     json.dump(jfig, outfile)
    #     outfile.close()
    # Validate
    assert calculated_chart == expected_chart
    # Teardown

def test_plotNodeMap(request, parent):
    ''' This method tests the node map figure  '''
    # Setup
    posted_num = pd.read_json(request.config.cache.get("posted_nums", None), orient='table').set_index('Date')
    with open(r"./cvai/data/testsets/nodemap.pickle", "rb") as infile:
        expected_chart = pickle.load(infile)
    # Exercise
    calculated_chart = pnm.createMap(posted_num, parent)
    # with open(r"./cvai/data/testsets/nodemap.pickle", "wb") as outfile:
    #     pickle.dump(calculated_chart, outfile)
    # Validate
    assert calculated_chart == expected_chart
    # Teardown

@pytest.mark.parametrize("pva, filegetter2, index_column",[(True,"FSOC PVA",'Scenario'),(False,'FSOC No PVA','Date')],ids=['Plan V Actuals', 'Period v Period'], indirect=['filegetter2'])
def test_filterSoc(request, startdate, enddate,pva, filegetter2, index_column):
    '''    This method tests the filtering for the waterfall  '''
    # Setup
    expected_df = pd.read_csv(filegetter2.get('file_loc'), parse_dates=['Date'], index_col=index_column)
    posted_drivers = pd.read_csv(r'./cvai/data/Drivers_Revenue_Scenario.csv', parse_dates=True, index_col='Date')

    # Exercise
    calculated_df = wft.FilterSOCdates(posted_drivers, startdate, enddate, pva)
    calculated_df.to_csv(r'./cvai/data/testsets/fsoc.csv')
    # Validate
    assert pd.testing.assert_frame_equal(calculated_df,expected_df) is None
    # Teardown
#     assert 0

@pytest.mark.parametrize("pva,filegetter2",[(True,"Waterfall PVA"),(False,"Waterfall No PVA")], ids=['WF Plan V Actuals', 'WF Period v Period'],indirect=['filegetter2'])
def test_get_waterfall(request, parent, pva, filegetter2):# will parametrize
    '''      '''
    # Setup
    if pva:
        DriversSorted = pd.read_csv(r'./cvai/data/fsoc_pva.csv', parse_dates=['Date'], index_col='Scenario')
    else:    
        DriversSorted = pd.read_csv(r'./cvai/data/fsoc_month_to_month.csv', parse_dates=['Date'], index_col='Date')
    expected_df = pd.read_csv(filegetter2.get('file_loc'),parse_dates=['Date'], index_col=0)
    # Exercise
    calculated_df = wft.get_waterfall(DriversSorted, is_sorted=False, parent_variable=parent, pva = pva)
    # calculated_df.to_csv(r'./cvai/data/testsets/waterfall.csv')
    # Validate
    assert pd.testing.assert_frame_equal(calculated_df,expected_df) is None
    # Teardown
  

@pytest.mark.parametrize('pva', [True,False], ids=['Plan V Actuals', 'Period v Period'])
def test_plotWaterfall(request, pva, enddate, parent):
    '''   This method tests the production of the waterfall chart by comparing figure dictionaries   '''
    # Setup
    if pva:
        dataset = pd.read_csv(r'./cvai/data/waterfall_pva.csv', parse_dates=['Date'], index_col='Scenario')
        filename = r'./cvai/data/testsets/waterfall_windows.pickle' if platform.system() == 'Windows' else r'./cvai/data/testsets/waterfall.pickle'
    else:    
        dataset = pd.read_csv(r'./cvai/data/waterfall_month_to_month.csv', parse_dates=['Date'], index_col='Date')
        filename = r'./cvai/data/testsets/waterfall_no_pva_windows.pickle' if platform.system() == 'Windows' else r'./cvai/data/testsets/waterfall_no_pva.pickle'
    with open(filename, "rb") as infile:
        expected_chart = pickle.load(infile)
    # Exercise
    calculated_chart = pwf.plotWaterfall(dataset, parent, pva, enddate)
    # with open(r"./cvai/data/testsets/waterfall_windows.pickle", "wb") as outfile:
    #     pickle.dump(calculated_chart, outfile)
    # Validate
    assert calculated_chart == expected_chart
    # Teardown


def test_PlotCoversheet(request):
    '''   This method tests the coversheet production   '''
    # Setup
    driver_parent = request.config.cache.get("driver", None)
    target_driver = request.config.cache.get("target_driver", None)
    target_num = request.config.cache.get("target_num", None)
    target_denom = request.config.cache.get("target_denom", None)
    posted_drivers = pd.read_json(request.config.cache.get("posted_drivers", None), orient='table').set_index('Date')
    posted_num = pd.read_json(request.config.cache.get("posted_nums", None), orient='table').set_index('Date')
    posted_denom = pd.read_json(request.config.cache.get("posted_denoms", None), orient='table').set_index('Date')
    dataset = pd.read_csv(r'./cvai/data/waterfall_pva.csv', parse_dates=['Date'])
    filename = r'./cvai/data/testsets/coversheet_windows.pickle' if platform.system() == 'Windows' else r'./cvai/data/testsets/coversheet.pickle'
    with open(filename, "rb") as infile:
        expected_chart = pickle.load(infile)
    # Exercise
    calculated_chart = pcs.plotCoverSheet(driver_parent, target_driver,target_num,target_denom, posted_drivers, posted_num, posted_denom,dataset)
    # with open(r"./cvai/data/testsets/coversheet.pickle", "wb") as outfile:
    #     pickle.dump(calculated_chart, outfile)
    # Validate
    assert calculated_chart == expected_chart
    # Teardown
#     assert 0

# def test_report_production():
#     '''      '''
    # Setup

    # Exercise

    # Validate
    # assert True
    # Teardown

