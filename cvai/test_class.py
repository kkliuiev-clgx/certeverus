
from datetime import datetime

import pytest
import object_copy as oc   

from sva import SVA3 as sv3

driver_dict = {"Revenue/Total Assets": "TESTNAME"}
class TestClass:
    
    params = {
        "test_driverparent": [dict(a="Revenue", b="Revenue"), dict(a="Gross Profit", b="Gross Profit")],
        "test_scenario": [dict(a="ACTUALS", b="ACTUALS"), dict(a="PLAN", b="PLAN")],
        "test_companyname": [dict(a="ACN", b="ACN"), dict(a="GOOG", b="GOOG")],
        "test_daterange": [dict(a="2020-01-01", b="2021-09-30"), dict(a="1990-01-01", b="2021-01-01")],
        "test_driverlabel": [dict(a="Revenue/Total Assets"), dict(a="Gross Profit/Revenue")]
    }
    def test_driverparent(self, a, b):
        import cvai.singleFactorTransformation as sft
        guru_data = oc.Metric("client","params", "2020-01-01", "2021-09-30", "Garcia", "ACTUALS", "ACN", a, gf=True)
        d_driver = oc.Driver(guru_data,["EBITDA", "Gross Profit", "Revenue", "Total Assets"], 1)
        driverParent,_,_,_,_,_  = sft.get_SingleFactor(d_driver.driver,d_driver.driver, d_driver.driver, d_driver.driver_only.columns, driver_choice='Revenue/Total Assets')
        assert driverParent == b
    
    def test_scenario(self, a, b):
        import cvai.singleFactorTransformation as sft
        guru_data = oc.Metric("client","params", "2020-01-01", "2021-09-30", "Garcia", a, "ACN", "Revenue", gf=True)
        d_driver = oc.Driver(guru_data,["EBITDA", "Gross Profit", "Revenue", "Total Assets"], 1)
        driverParent, targetDriver,targetNum,targetDenom, postedDrivers, postedNum, postedDenom = sft.get_SingleFactor(d_driver.driver,d_driver.driver, d_driver.driver, d_driver.driver_only.columns, driver_choice='Revenue/Total Assets')
        assert postedDrivers.Scenario.unique()[0] == b
    
    def test_companyname(self, a, b):
        import cvai.singleFactorTransformation as sft
        guru_data = oc.Metric("client","params", "2020-01-01", "2021-09-30", "Garcia", "ACTUALS", a, "Revenue", gf=True)
        d_driver = oc.Driver(guru_data,["EBITDA", "Gross Profit", "Revenue", "Total Assets"], 1)
        driverParent, targetDriver,targetNum,targetDenom, postedDrivers, postedNum, postedDenom = sft.get_SingleFactor(d_driver.driver,d_driver.driver, d_driver.driver, d_driver.driver_only.columns, driver_choice='Revenue/Total Assets')
        assert postedDrivers.Name.unique()[0] == b
    
    def test_daterange(self, a, b):
        import cvai.singleFactorTransformation as sft
        guru_data = oc.Metric("client","params", a, b, "Garcia", "ACTUALS", "ACN", "Revenue", gf=True)
        d_driver = oc.Driver(guru_data,["EBITDA", "Gross Profit", "Revenue", "Total Assets"], 1)
        driverParent, targetDriver,targetNum,targetDenom, postedDrivers, postedNum, postedDenom = sft.get_SingleFactor(d_driver.driver,d_driver.driver, d_driver.driver, d_driver.driver_only.columns, driver_choice='Revenue/Total Assets')
        assert postedDrivers['Date'].between(a, b, inclusive=True)

# TEST IF THE LABEL FOR THE DRIVER IS SUCCESSFULLY REPLACED
def test_driverlabel():
    import cvai.singleFactorTransformation as sft
    guru_data = oc.Metric("client","params", "2020-01-01", "2021-09-30", "Garcia", "ACTUALS", "ACN", "Revenue", gf=True)
    d_driver = oc.Driver(guru_data,["EBITDA", "Gross Profit", "Revenue", "Total Assets"], 1)
    label = driver_dict.get(list(d_driver.driver.columns)[-1])
    driverParent, targetDriver,targetNum,targetDenom, postedDrivers, postedNum, postedDenom = sft.get_SingleFactor(d_driver.driver, d_driver.driver, d_driver.driver, d_driver.driver_only, driver_choice="Revenue/Total Assets", driver_label=label)
    assert targetDriver == "TESTNAME"

    
def test_object_creation():
    '''      '''
    # Setup

    # Exercise
    a = oc.Metric("client","params", "2020-01-01", "2021-09-30", "Garcia", "ACTUALS", "ACN","Revenue")
    print(a.data)
    # Validate
    assert True
    
    # Teardown
# a = Metric("client","params", "startdate", "enddate", "Ianova", "scenario")
# print(a.data)

@pytest.mark.parametrize("gfcase", [True, False]) 
def test_gurufocus_object(gfcase):
    # Setup

    # Exercise
    b = oc.Metric("client","params", "2020-01-01", "2021-09-30", "Garcia", "ACTUALS", "ACN", "Revenue", gf=gfcase)
    print(b.data)
    # Validate
    assert True
    
    # Teardown

@pytest.mark.parametrize("case", [1,2,3]) 
def test_driver(case):
    # Setup
    guru = oc.Metric("client","params", "2020-01-01", "2021-09-30", "Garcia", "ACTUALS", "ACN", "Revenue", gf=True)
    # Exercise
    d = oc.Driver(guru, ["EBITDA", "Gross Profit", "Revenue", "Total Assets"], case)
    # Validate
    assert d.driver[0] == 30.2/124.0
    # Teardown
    print("End test")

def test_singlefactor(): #TODO #370 Parameterize the test for different data sources and numerator denominatori combos
    '''      '''
    # Setup
    import os
    import cvai.singleFactorTransformation as sft
    import cvai.PlotSingleFactor as psf
    from core.utils import get_engine

    db = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'certeverus',
            'USER': 'db',
            'PASSWORD': 'certeverus',
            'HOST': 'db' if os.environ.get("DOCKER") else 'localhost',
            'PORT': 5432,
        }
    }

    # import urllib.request
    # link = "https://banks.data.fdic.gov/api/institutions?filters=STALP%3AIA%20AND%20ACTIVE%3A1&fields=ZIP%2COFFDOM%2CCITY%2CCOUNTY%2CSTNAME%2CSTALP%2CNAME%2CACTIVE%2CCERT%2CCBSA%2CASSET%2CNETINC%2CDEP%2CDEPDOM%2CROE%2CROA%2CDATEUPDT%2COFFICES&sort_by=OFFICES&sort_order=DESC&limit=10&offset=0&format=csv&download=false&filename=data_file"

    # with urllib.request.urlopen(link) as url:    
    #     s = url.read()
    # # I'm guessing this would output the html source code ?
    # print(s)

    guru_data = oc.Metric("client","params", "2020-01-01", "2021-09-30", "Garcia", "ACTUALS", "ACN", "Revenue", gf=True)
    d_driver = oc.Driver(guru_data,["EBITDA", "Gross Profit", "Revenue", "Total Assets"], 1)
    # Exercise
    driverParent, targetDriver,targetNum,targetDenom, postedDrivers, postedNum, postedDenom = sft.get_SingleFactor(d_driver.driver,d_driver.driver, d_driver.driver, d_driver.driver_only.columns, driver_choice='Revenue/Total Assets')
    plot_fig = psf.plotSingleFactor(driverParent, targetDriver,targetNum,targetDenom, postedDrivers, postedNum, postedDenom, 1)
    print(plot_fig)
    x = db
    print(x)
    engine = get_engine()
    #plot_fig.show()
    # Validate
    assert targetDriver == "Revenue/Total Assets"
    # Teardown


### Parametrizing test methods through per-class configuration

# def pytest_generate_tests(metafunc):
#     funcarglist = metafunc.cls.params[metafunc.function.__name__]
#     argnames = sorted(funcarglist[0])
#     metafunc.parametrize(
#         argnames, [[funcargs[name] for name in argnames] for funcargs in funcarglist]
#     )

