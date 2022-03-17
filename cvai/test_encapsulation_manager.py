'''  '''
import pickle
import unittest
import json
import os
# import plotly

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
import cvai.EncapsulationManager as em 
from core.utils import get_engine


drivers = pd.read_csv(r'./cvai/data/Tutorial_data/tutorial_drivers.csv')
plan = pd.read_csv(r'./cvai/data/testsets/plan.csv', parse_dates=['Date'], index_col='Date')
df = pd.read_csv(r'./cvai/data/Tutorial_data/tutorial_POS_data_v2.csv')


def test_clean_data(request):
    '''      '''
    # Setup
    expected_df = pd.read_csv(r'./cvai/data/expected_df_full_cleaned.csv', parse_dates = False, index_col=0)
    # Exercise
    calculated_df = em.clean_data(df)
    # calculated_df.to_csv(r'./cvai/data/expected_df_full_cleaned.csv')

    # Validate
    assert pd.testing.assert_frame_equal(calculated_df,expected_df) is None
    # Teardown
    request.config.cache.set("df", calculated_df.to_json(orient='table'))

     
def test_combine_data(request):
    '''      '''
    # Setup
    df = pd.read_json(request.config.cache.get("df", None), orient='table').set_index('Date')
    expected_df = pd.read_csv(r'./cvai/data/encap_df.csv', parse_dates=['Date'], index_col=('Date'))
    cols = expected_df.columns
    expected_df[cols] = expected_df[cols].astype(str,errors='ignore')
    # Exercise
    calculated_df = em.combine_data(df, plan)
    calccols = calculated_df.columns
    calculated_df[calccols] = calculated_df[calccols].astype(str,errors='ignore')
    # calculated_df.to_csv(r'./cvai/data/calc_encap_df.csv')

    # Validate
    assert pd.testing.assert_frame_equal(calculated_df,expected_df, check_dtype=False) is None
    # Teardown
    
def test_pass_prepared_data():
    '''      '''
    # Setup


    # Exercise
    calculated_df = em.pass_prepared_data(engine=None,
            save_data_to="csv",
            source="local",
            client='Test',)

    # Validate
    assert True

    # Teardown
    if os.path.exists(r"./cvai/dfclean.csv"):
        os.remove(r"./cvai/dfclean.csv")
    else:
        print("The file does not exist")