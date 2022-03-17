import pandas as pd
import os 

try:
    import ingest_local_textdata as ilt
    import ingest_financial_statement as ift
except ImportError:
    from cvai import ingest_local_textdata as ilt
    from cvai import ingest_financial_statement as ift

df = pd.read_csv("cvai/data/sourcing_actuals.csv", index_col=['Date'], parse_dates=['Date','Req_Date', 'Order_Date'])

currency_cols = ['PO_Cost', 'Quantity']
for i in currency_cols:
    df = ift.clean_currency(df,i)

df['Scenario'] = 'ACTUALS'

df.to_csv('cvai/data/sourcing_input.csv')
print()
