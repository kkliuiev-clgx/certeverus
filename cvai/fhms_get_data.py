
import pandas as pd
import os
import EncapsulationManager as em

def get_Data():
        
    if not os.path.isfile('dfclean.csv'):
        print('No Local File')
        print('Getting data')
        drivers, df, plan  = em.pass_prepared_data() #loads the data frames for resampling
    else:
        print('Reading Locally')
        drivers = pd.read_csv('drivers.csv', parse_dates=True)
        df = pd.read_csv('dfclean.csv', parse_dates=True, index_col='Date')
        plan = pd.read_csv('plan.csv', parse_dates=True, index_col='Date')
    
    return drivers, df, plan

drivers, df, plan  = get_Data()
df.to_csv(r'./catch/actuals_and_plan_inGetData21.csv')