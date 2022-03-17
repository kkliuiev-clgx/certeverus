import pytest
import pandas as pd

@pytest.fixture
def FHMS_drivers():
    return pd.read_csv(r'./cvai/data/FHMS_Drivers_v3.csv') #can this be a fixture?

@pytest.fixture
def FHMS_parent():
    return 'Free Cash Flow'

@pytest.fixture
def drivers():
    return pd.read_csv(r'./cvai/data/Tutorial_data/tutorial_drivers.csv') #can this be a fixture?

@pytest.fixture (params=['Revenue'])
def parent(request):
    return request.param

@pytest.fixture
def expected_parent_FHMS():
    return pd.read_csv(r'./cvai/data/filtered_drivers_FHMS.csv', index_col=0)

@pytest.fixture
def expected_parent():
    return pd.read_csv(r'./cvai/data/filtered_drivers.csv')

@pytest.fixture
def startdate():
    return '2020-08-01'

@pytest.fixture
def enddate():
    return '2020-09-30'

@pytest.fixture
def expected_nums():
    exp_nums=pd.read_csv(r'./cvai/data/nums.csv')
    # expected_nums_list = exp_nums.Metric.unique().tolist()
    return exp_nums

@pytest.fixture
def expected_dens():
    exp_dens=pd.read_csv(r'./cvai/data/dens.csv')
    # expected__list = exp_nums.Metric.unique().tolist()
    return exp_dens
    
@pytest.fixture
def expected_df():
    exp_df=pd.read_csv(r'./cvai/data/expected_df.csv',parse_dates=True, index_col='Date')
    # expected__list = exp_nums.Metric.unique().tolist()
    return exp_df

# @pytest.fixture
# def expected_df_full():
#     exp_df=pd.read_csv(r'./cvai/data/expected_df_full.csv',parse_dates=True, index_col='Date')
#     # expected__list = exp_nums.Metric.unique().tolist()
#     return exp_df

@pytest.fixture
def expected_df_full_for_aug_sep_2020():
    exp_df=pd.read_csv(r'./cvai/data/expected_df_full_aug_sep_2020.csv',parse_dates=True, index_col='Date').apply(pd.to_numeric,errors='ignore')
    # expected__list = exp_nums.Metric.unique().tolist()
    return exp_df

@pytest.fixture
def demo_data():
    demo_data_df = pd.read_csv(r'./cvai/data/Test_data_plan_and_actuals.csv', parse_dates=True, index_col='Date')
    return demo_data_df

@pytest.fixture
def desired_dictionary():
    return {'Revenue': 'sum', 'Items': 'sum', 'SKU': 'nunique', 'Invoice': 'nunique', 'Product Line': 'nunique', 
    'Account': 'nunique', 'Rep': 'nunique', 'Manager': 'nunique', 'Team': 'nunique', 'Market': 'nunique'}


@pytest.fixture(params=['Revenue','SKU'])
def numers(request):
    ''' This returns a fixed set for testing'''
    return request.param

@pytest.fixture(params=[['Scenario'], ['Scenario', 'CAE']], ids=['No Attributes', 'Attributes'])
def group_list(request):
    return request.param

# @pytest.fixture()
# def expected_ytd():
#     return r'./cvai/data/expected_resample_with_ytd.csv'

@pytest.fixture
def fixt(request):
    return request.param * 3

@pytest.fixture
def file_dictionary():
    return{'YTD w Revenue':{'ytd_sel':True,'file_loc':r'./cvai/data/expected_resample_with_ytd.csv'},
                'NOT YTD w Revenue':r'./cvai/data/expected_resample.csv',
                'Demo_Data':r'./cvai/data/Test_data_plan_and_actuals.csv',
                'Aug-Sept2020':r'./cvai/data/expected_df_full_aug_sep_2020.csv',
                'Full_data':r'./cvai/data/expected_df_full.csv',
                'NOT YTD w SKU':r'./cvai/data/agg_sku_scenario_aug_sep_actuals.csv'
                }

@pytest.fixture
def file_dictionary2():
    return{
        'Revenue, Scenario, YTD':{'ytd_sel':True,'file_loc':r'./cvai/data/expected_resample_ytd_revenue_scenario.csv', 'group_sel':['Scenario'],'numers_sel':'Revenue'},
        'Revenue, Scenario':{'ytd_sel':False,'file_loc':r'./cvai/data/expected_resample_monthly_reveneue_scenario.csv', 'group_sel':['Scenario'],'numers_sel':'Revenue'},
        'SKU, Scenario':{'ytd_sel':False,'file_loc':r'./cvai/data/expected_resample_monthly_SKU_scenario.csv', 'group_sel':['Scenario'],'numers_sel':'SKU'},
        'SKU, Scenario, YTD':{'ytd_sel':True,'file_loc':r'./cvai/data/expected_resample_YTD_SKU_scenario.csv', 'group_sel':['Scenario'],'numers_sel':'SKU'},
        'Revenue, ScenarioCAE, YTD':{'ytd_sel':True,'file_loc':r'./cvai/data/expected_resample_YTD_Revenue_scenarioCAE.csv', 'group_sel':['Scenario','CAE'],'numers_sel':'Revenue'},
        'Revenue, ScenarioCAE':{'ytd_sel':False,'file_loc':r'./cvai/data/expected_resample_monthly_Revenue_scenarioCAE.csv', 'group_sel':['Scenario','CAE'],'numers_sel':'Revenue'},
        'SKU, ScenarioCAE, YTD':{'ytd_sel':True,'file_loc':r'./cvai/data/expected_resample_YTD_SKU_scenarioCAE.csv', 'group_sel':['Scenario','CAE'],'numers_sel':'SKU'},
        'SKU, ScenarioCAE':{'ytd_sel':False,'file_loc':r'./cvai/data/expected_resample_monthly_SKU_scenarioCAE.csv', 'group_sel':['Scenario','CAE'],'numers_sel':'SKU'},
        'Filter SKU, ScenarioCAE':{'ytd_sel':False,'file_loc':r'./cvai/data/Filter_SKU_ScenarioCAE.csv', 'group_sel':['Scenario','CAE'],'numers_sel':'SKU'},
        'Filter Revenue, ScenarioCAE':{'ytd_sel':False,'file_loc':r'./cvai/data/Filter_Revenue_ScenarioCAE.csv', 'group_sel':['Scenario','CAE'],'numers_sel':'Revenue'},
        'Filter SKU, Scenario':{'ytd_sel':False,'file_loc':r'./cvai/data/Filter_SKU_Scenario.csv', 'group_sel':['Scenario'],'numers_sel':'SKU'},
        'Filter Revenue, Scenario':{'ytd_sel':False,'file_loc':r'./cvai/data/Filter_Revenue_Scenario.csv', 'group_sel':['Scenario'],'numers_sel':'Revenue'},
        'Drivers, Revenue, Scenario, YTD':{'ytd_sel':True,'file_loc':r'./cvai/data/Drivers_Revenue_Scenario_YTD.csv', 'group_sel':['Scenario'],'numers_sel':'Revenue'},
        'Drivers, Revenue, Scenario':{'ytd_sel':False,'file_loc':r'./cvai/data/Drivers_Revenue_Scenario.csv', 'group_sel':['Scenario'],'numers_sel':'Revenue'},       
        'Drivers, SKU, Scenario':{'ytd_sel':False,'file_loc':r'./cvai/data/Drivers_Revenue_Scenario.csv', 'group_sel':['Scenario'],'numers_sel':'SKU'},
        'Drivers, SKU, Scenario, YTD':{'ytd_sel':True,'file_loc':r'./cvai/data/Drivers_Revenue_Scenario_YTD.csv', 'group_sel':['Scenario'],'numers_sel':'SKU'},
        'Drivers, Revenue, ScenarioCAE, YTD':{'ytd_sel':True,'file_loc':r'./cvai/data/Drivers_Revenue_ScenarioCAE_YTD.csv', 'group_sel':['Scenario','CAE'],'numers_sel':'Revenue'},
        'Drivers, Revenue, ScenarioCAE':{'ytd_sel':False,'file_loc':r'./cvai/data/Drivers_Revenue_ScenarioCAE.csv', 'group_sel':['Scenario','CAE'],'numers_sel':'Revenue'},       
        'Drivers, SKU, ScenarioCAE':{'ytd_sel':False,'file_loc':r'./cvai/data/Drivers_Revenue_ScenarioCAE.csv', 'group_sel':['Scenario','CAE'],'numers_sel':'SKU'},
        'Drivers, SKU, ScenarioCAE, YTD':{'ytd_sel':True,'file_loc':r'./cvai/data/Drivers_Revenue_ScenarioCAE_YTD.csv', 'group_sel':['Scenario','CAE'],'numers_sel':'SKU'},
        'Drive_x2_input':{'ytd_sel':True,'file_loc':r'./cvai/data/Driver_x.csv', 'group_sel':['Scenario','CAE'],'numers_sel':'SKU'},
        'Create_driver_input':{'ytd_sel':True,'file_loc':r'./cvai/data/Driver_x.csv', 'group_sel':['Scenario','CAE'],'numers_sel':'SKU'},
        'FSOC PVA':{'ytd_sel':False,'file_loc':r'./cvai/data/fsoc_pva.csv', 'group_sel':['Scenario'],'numers_sel':'Revenue'},
        'FSOC No PVA':{'ytd_sel':False,'file_loc':r'./cvai/data/fsoc_month_to_month.csv', 'group_sel':['Scenario'],'numers_sel':'Revenue'},
        'Waterfall PVA':{'ytd_sel':False,'file_loc':r'./cvai/data/waterfall_pva.csv', 'group_sel':['Scenario'],'numers_sel':'Revenue'},
        'Waterfall No PVA':{'ytd_sel':False,'file_loc':r'./cvai/data/waterfall_month_to_month.csv', 'group_sel':['Scenario'],'numers_sel':'Revenue'},
        'Waterfall Chart PVA':{'ytd_sel':False,'file_loc':r'./cvai/data/testsets/waterfall.pickle', 'group_sel':['Scenario'],'numers_sel':'Revenue'},
        'Waterfall Chart No PVA':{'ytd_sel':False,'file_loc':r'./cvai/data/testsets/waterfall_no_pva.pickle', 'group_sel':['Scenario'],'numers_sel':'Revenue'}
    }

@pytest.fixture
def filegetter2(request, file_dictionary2):
    passed_dict = file_dictionary2.get(request.param)
    # df = pd.read_csv(key_name,parse_dates=True, index_col='Date')
    print(f'{passed_dict} =')
    return passed_dict


@pytest.fixture
def filegetter(request, file_dictionary):
    # passed_dict = file_dictionary.get(request.param)
    df = pd.read_csv(key_name,parse_dates=True, index_col='Date')
    return df

def pytest_generate_tests(metafunc):
    if "ytd_set" in metafunc.fixturenames:
        metafunc.parametrize("ytd_set", [True, False], ids=('YTD','NOT YTD'))
    if "group_set" in metafunc.fixturenames:
        metafunc.parametrize("group_set", [['Scenario'],['Scenario', 'CAE']], ids=('No Attributes','With Attributes'))
    if "numers_set" in metafunc.fixturenames:
        metafunc.parametrize("numers_set", ['Revenue','SKU'])

def make_dictionary(ytd,numers,groups,files):
    import itertools
    
    # result contains all possible combinations.
    combinations = tuple(itertools.product(ytd,numers,groups))
    # print(combinations, files) 
    # print(len(combinations))

    mydict = dict(zip(files, combinations))
    # print(mydict)
    return mydict


@pytest.fixture
def filenamegetter(request):
    ytd = (True,False)
    numers = ['Revenue','SKU']
    print(numers)
    groups = [['Scenario'],['Scenario','CAE']]
    files= tuple(['file1','file2','file3','file4','file5','file6','file7','file8'])
   
    mydict = make_dictionary(ytd, numers, groups, files)
    print(mydict)
    lst = request.param
    print(lst)
    expected = ([k for k, v in mydict.items() if v == lst]).pop()
    return expected

@pytest.fixture
def file_filtered_raw():
    ytd = [False]
    numers = ('Revenue','SKU')
    groups = [['Scenario'],['Scenario','CAE']]
    files= tuple(['file1','file2','file3','file4'])
    mydict = make_dictionary(ytd,numers,groups,files)
    print(mydict)
    lst_raw = request.param
    expected = ([k for k, v in mydict.items() if v == lst_raw]).pop()
    print(expected)
    return expected

@pytest.fixture
def drivex():
    return pd.read_csv(r'./cvai/data/Drivers_Revenue_ScenarioCAE_YTD.csv',parse_dates=True, index_col='Date')

# ytd = [False]
# numers = ['Revenue','SKU']
# groups = [['Scenario'],['Scenario','CAE']]
# files= tuple(['file1a','file2a','file3a','file4a'])

# mydict = make_dictionary(ytd, numers, groups, files)
# print(f'{mydict=}')