import pandas as pd
import itertools
import numpy as np
from datetime import datetime
from operator import itemgetter

class myDict(dict):

    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value



def generate_segment_plan_data(customer_dict):
    
    df = []
    vals = itemgetter('segments','scenarios','dates', 'branches')(customer_dict)
    data = list(itertools.product(*vals))
    # print(data)
    df = pd.DataFrame(data, columns=['Segments','Scenario','Date', 'Branch']).set_index('Date')
    # df['Customers_Size'] = df.Scenario.apply(lambda x: np.random.randint(.975*customer_dict.get('customer_base'), 1.025*customer_dict.get('customer_base'))if x == 'ACTUALS' else customer_dict.get('customer_base'))
    
    df['Customers_Size'] = (df.Scenario.apply(lambda x: np.random.uniform(*(customer_dict.get('randomizer').get(x))))*customer_dict.get('customer_base')).astype(int)
    df['Segment_Split'] = df.Segments.map(customer_dict.get('numbers'))
    df['Customers'] = df.Customers_Size*df.Segment_Split
    df['Users_Added'] = (df.Scenario.apply(lambda x: np.random.uniform(0.0, customer_dict['max_adoption']/len(df)) if x == 'ACTUALS' else customer_dict['max_adoption']/len(df))*df.Customers).astype(int)
    df['Carefull_Budget'] = df.Scenario.map(customer_dict.get('price')) * df.Users_Added
    df['Transitioned_Accounts'] = df.Scenario.apply(lambda x:np.random.uniform(*(customer_dict.get('mortality').get(x))))*df.Users_Added
    df['Beginning_Value'] = df.Segments.map(customer_dict.get('Avg_account_holdings'))*df.Transitioned_Accounts
    df['Beneficiaries'] = df.Scenario.apply(lambda x: np.random.uniform(1.2, 1.4) if x == 'ACTUALS' else 1.3)*df.Transitioned_Accounts
    df['Retained_Value'] = df.Scenario.apply(lambda x: np.random.uniform(*(customer_dict.get('Retention_percentage').get(x))))*df.Beginning_Value #TODO #375 Adjust to be on the Mort Adj Value and see where this makes sense
    df['Income_Producing_Assets'] = df.Scenario.apply(lambda x: np.random.uniform(*(customer_dict.get('LTV').get(x))))*df.Retained_Value # TODO #376 Randomize for ACTUALs
    df['Income']= df.Scenario.apply(lambda x: np.random.uniform(.025,.032) if x == 'ACTUALS' else customer_dict.get('margin'))*df.Income_Producing_Assets
    # df['Branch']= np.random.choice(customer_dict.get('branches'),len(df))
    df['Days_Retained']= df.Scenario.apply(lambda x: np.random.uniform(*(customer_dict.get('Days_Retained').get(x))))
    df['Remaining_Beneficiaries']= df.Scenario.apply(lambda x: np.random.uniform(*(customer_dict.get('Remaining_Beneficiaries').get(x))))*df['Beneficiaries']

    return df

#  Set Variables and Dictionary

def set_customer_info():
    customer_dict = myDict()
    customer_dict.add('customer_base',75000)
    customer_dict.add('numbers',{'Segment A':.2, 'Segment B':.5, 'Segment C':.3}) # TODO #377 Add total size of market (20/50/30 @ 120/60/25)
    customer_dict.add('randomizer',{'BASELINE':[.975,1.025],'PLAN':[1,1],'ACTUALS':[.975,1.025], 'CONTROL':[.975,1.025]})
    customer_dict.add('price', {'BASELINE':0,'PLAN':14.95,'ACTUALS':14.95, 'CONTROL':0})#The Carefull price per month for a user
    customer_dict.add('max_adoption',.25) # Maximum adoption (CIF = Customer information File)
    customer_dict.add('Avg_account_holdings',{'Segment A':120000,'Segment B':60000, 'Segment C':25000}) # Average value of account holdings per customer 
    customer_dict.add('Retention_percentage',{'BASELINE':[.05,.075],'PLAN':[.95,.95],'CONTROL':[.05,.075], 'ACTUALS':[.925,.975]}) # TODO #378 Possibly do a Baseline Case
    customer_dict.add('LTV',{'BASELINE':[.825,.875],'PLAN':[.85,.85],'CONTROL':[.825,.875], 'ACTUALS':[.825,.875]}) # TODO #379 Randomize for ACTUALS
    customer_dict.add('margin',.03)
    customer_dict.add('segments',['Segment A','Segment B','Segment C'])
    customer_dict.add('branches', ['Branch_1','Branch_2', 'Branch_3'])
    customer_dict.add('scenarios',['PLAN', 'ACTUALS', 'BASELINE', 'CONTROL']) #TODO Add a control group 
    customer_dict.add('mortality', {'BASELINE':[.25,.275],'PLAN':[.25,.25],'CONTROL':[.25,.275], 'ACTUALS':[.25,.275]})
    # date_range = pd.date_range('2021-09-01','2023-12-01', freq='M').tolist()
    customer_dict.add('dates', pd.date_range('2020-09-01','2024-12-01', freq='M').tolist())
    customer_dict.add('Days_Retained', {'BASELINE':[30,60],'PLAN':[270,270],'CONTROL':[30,60], 'ACTUALS':[180,360]})
    customer_dict.add('Remaining_Beneficiaries', {'BASELINE':[.1,.3],'PLAN':[.45,.45],'CONTROL':[.10,.30], 'ACTUALS':[.45]})
# remaining beneficiaries of total beneficiaries  0% in baseline / 66%+- in Actuals, 0% in control group 66% static in plan  
# days 90 days for mortality in baseline and control group/plan and the actuals 360 days (randomized for actuals and static for plan)
#  
    
    return customer_dict

# Execute

customer_dict = set_customer_info()
df = generate_segment_plan_data(customer_dict)
df.to_csv('Alloy_Carefull_revised.csv')
# print(f'This is the {df=} and {customer_dict=}')

