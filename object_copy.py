import pandas as pd
import simplejson as json
from datetime import datetime
# import core as cr
from core.utils import get_engine
from cvai import transformation_manager as tm
from sva import SVA3 as sv3

class Metric:
    ''' Base object used for storing the (planned/actual) data of a company (single/averaged) '''

    def __init__(self, client, params, startdate, enddate, metric, scenario, companyname, parent, gf=True):
        self.client = client
        self.startdate = datetime.strptime(startdate, "%Y-%m-%d")
        self.enddate = datetime.strptime(enddate, "%Y-%m-%d")
        self.metric = metric
        self.scenario = scenario
        self.companyname = companyname
        self.parent = parent
        self.num = ["Revenue"]
        self.den = ["Items"]
        # self.data = self.get_data(self.metric)
        # self.drivers = self.get_drivers(self.parent)
        if gf:
            dataf = sv3.Load.LoadGuruFocus()
            dataf = dataf.pivot(index=('Date', 'Name'),
                columns='Metric', values='value').reset_index()
            self.data = dataf.loc[(dataf['Date'] >= self.startdate) & (dataf['Date'] <= self.enddate) & (dataf['Name'] == self.companyname)]
            self.data['Parent'] = self.parent
            self.data['Scenario'] = self.scenario
        else:
            self.data = self.get_data(self.metric)
   
    def get_data(self, metric): #TODO #371 connect Object Copy to Postgres SQL data base for the third case.
        df = pd.read_csv(
            r'cvai\data\Tutorial_data\tutorial_POS_data_v2.csv', parse_dates=True, index_col="Date"
            )
        df = df[df['CAE'] == metric]
        print(df.info())
        return df
    
    # def get_drivers(self, parent):
    #     drivers = pd.read_csv(
    #         r'cvai\data\Tutorial_data\tutorial_drivers.csv'
    #         )
    #     drivers = drivers.loc[drivers['Parent'] == parent].reset_index(drop=True)
    #     return drivers

class Driver:
    ''' Creates a driver using a given Metric object, list of metrics, and a case number'''

    def __init__(self, data, metrics_list, case):
        self.data = data
        self.metrics_list = metrics_list
        self.case = case
        self.driver, self.driver_only = self.create_drivers(self.data, self.metrics_list, self.case)

    def create_drivers(self, data, metrics_list, case):
        val = data.data.copy()
        drivers_only = pd.DataFrame()
        fixedval = metrics_list[0]
        while len(metrics_list) >= 2: 
            column_name = self.get_column_name(metrics_list, fixedval, case)
            val[column_name] = self.get_column_value(data, metrics_list, fixedval, case)
            drivers_only[column_name] = self.get_column_value(data, metrics_list, fixedval, case)
            # drivers_only[column_name]=
            metrics_list.pop(0)
        return val, drivers_only

    def get_column_name(self, metrics_list, fixedval, case):
        if case == 1:
            column_name = metrics_list[0]+"/"+metrics_list[1]
        elif case == 2:
            column_name = fixedval+"/"+metrics_list[1]
        else:
            column_name = metrics_list[1]+"/"+fixedval
        return column_name

    def get_column_value(self, data, metrics_list, fixedval, case):
        column_val =  pd.DataFrame()
        if case == 1:
            column_val = data.data[metrics_list[0]]/data.data[metrics_list[1]]
        elif case == 2:
            column_val = data.data[fixedval]/data.data[metrics_list[1]] 
        else:
            column_val = data.data[metrics_list[1]]/data.data[fixedval] 
        return column_val
    
