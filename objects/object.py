import pandas as pd
import simplejson as json
from core.utils import get_engine
from cvai import transformation_manager as tm

class Metric:

    def __init__(self, client, params, startdate, enddate, metric, scenario):
        self.startdate = startdate
        self.enddate = enddate
        self.metric = metric
        self.scenario = scenario
        self.drivers = self.get_drivers(client, startdate, enddate, metric, scenario)
    
    def get_drivers(self, client, params, startdate, enddate, metric, scenario):
        engine = get_engine()
        parent = params.get("parent")
        resample_period = params.get("resample_period")
        ytd = params.get("ytd", "false") == "true"
        drivers = pd.read_sql_table(client.get_drivers_table_name(), engine, parse_dates=True)
        df = pd.read_sql_table(client.get_dfclean_table_name(), engine, parse_dates=True, index_col='Date')
        if client.name.strip() =='FHMS':
            DriversFile= tm.CreateDrivers(drivers, df, parent, resample_period, scenario, startdate, enddate, ytd)
        else:
            DriversFile = tm.create_drivers(df,drivers, parent, resample_period, scenario, startdate, enddate, ytd)    
        return DriversFile


a = Metric(client, params, startdate, enddate, metric, scenario)
a == a