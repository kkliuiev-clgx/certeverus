import pandas as pd
import os
import Waterfall_Transformation as wt
import transformation_manager as tm
import filter_manager as fm
import PlotWaterfall as pwf

def count_unique_actuals(md, scenario='ACTUALS', target='Provider'):
    md['Date'] = pd.to_datetime(md.Date)
    mdx = md.set_index('Date', drop=True)
    mdr= mdx[mdx.Scenario == scenario].resample('M').nunique()
    mdr['variable']= target+"s"
    mdr['Scenario']= scenario
    mdr['value'] = mdr[target]
    mdrf = mdr[['variable', 'value', 'Scenario']].reset_index()
    return mdr

# print(count_unique_actuals(md))

def remove_future_actuals(md):
    print(md.info())
    md['Date'] = pd.to_datetime(md['Date'])
    max_actuals_date = md['Date'][(md['variable']=='Free Cash Flow')&(md['Scenario']=='ACTUALS')].max()
    print(str(max_actuals_date),"is now")
    md_trimmed = md[md['Date'] <= max_actuals_date]
    return md_trimmed

def cagr(start_value, end_value, num_periods): #function to produce a CAGR
    ''' This function produces a CAGR.  It can be used with other functions to 
    filter time periods, drivers, Numerators and other attributes
    '''
    return (end_value / start_value) ** (1 / (num_periods - 1)) - 1 

# def get_ytd(dframe, startex='2020-06-01', endex='2020-10-31'):
#     # md['Date'] = pd.to_datetime(md.Date)
#     # mdx = md.set_index('Date', drop=True)
#     dframe = dframe.drop(columns='index')
#     dframe_ytd = dframe.loc[startex:endex].groupby(['Scenario','variable']).sum()
#     dframe_ytd['Date'] = '2020-10-01'
#     dframe_ytd['Date'] = pd.to_datetime(dframeytd['Date'])
#     dframe_ytd = dframe_ytd.reset_index()
#     dframe_ytd = dframe_ytd.set_index('Date', drop=True)
#     print("THE YTD DF:\n",dframe_ytd)
#     return dframe_ytd

selected='Net Revenue/Visit'
md = pd.read_csv(r"./dfclean.csv", parse_dates=True)
drivers = pd.read_csv(r"./drivers.csv", parse_dates=True)
# print(md, md.info())
md['Date'] = pd.to_datetime(md.Date)
mdt = md.set_index('Date', drop=True)
# mdt.to_csv(r'./catch/mdt.csv')

mdfilter, driver_parent, num, den = fm.filter_drivers(drivers, mdt, selected)
# ans = get_ytd(mdfilter)
# print("THE YTD DF:\n", ans)

mdf, numm, denn= tm.CreateDrivers(drivers, mdfilter, selected,'MS', startdate='2020-06-01', enddate='2020-10-31', ytd=False) # already drivers
# mdf.to_csv(r'./catch/mdf.csv')
# print("MDF is:\n",mdf)
r = wt.FilterSOCdates(mdf, start = "2020-10-01", end = "2020-10-01", pva = False)

# r.to_csv(r'./catch/r.csv')
print("R is:\n",r)

pwf.plotWaterfall(wt.get_waterfall(r,False, selected), selected)


