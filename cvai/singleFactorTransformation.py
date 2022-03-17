"""
This is how we will Transform the data for Singlefactor Drivers


Created on Sat Jul  4 12:25:10 2020

@author: michaelprinci
"""
import pandas as pd
from charts import utils

# try:	# if not os.path.isfile('dfcleaned.csv'):
#     from cvai import filter_manager as fm
#     from cvai import EncapsulationManager as em
# except ImportError:	# else:
#     import filter_manager as fm
#     import EncapsulationManager as em

def singlefactor_list(drivers_file, nums_file,denoms_file,drivers, driver_choice, attributes, driver_label):
    denom = driver_choice.rsplit("/")
    denom.extend([driver_choice, "Name", "Date", "Scenario"])
    drivers_holding = drivers_file.filter(items=[*denom]).set_index("Date") 

    driver_parent = drivers_file.Parent.unique()[0]
    target_num = driver_choice.rsplit("/")[0] #TODO #381 The label method needs to be adjusted with custom labels for Driversq
    target_denom = driver_choice.rsplit("/")[1]
    if attributes is not None:
        print(attributes)
    return driver_parent, driver_choice, target_num,target_denom, drivers_holding, drivers_holding, drivers_holding


def singlefactor_df(drivers_file, nums_file, denoms_file, drivers, driver_choice, attributes, driver_label):
    print(drivers)
    # 1. Get Drivers File Parent
    driver_parent = drivers_file.Parent.unique()[0]
    # print("FROM SFT:driverParent\n",driver_parent)
    # 2. Get list of names for driver
    # driver_list = drivers_file['Driver'].unique().tolist()
    # print("FROM SFT:driverList\n",driver_list)
    # 3. Select Driver from list and create dictionaries
    if driver_choice is None:
        driver_choice = input(" Pick one from the Driver List ")

    # print ("FROM SFT 42 Chosen driver is ",driver_choice, attributes)

    # 4. Filter drivers by df (see previous work)

    driver_filtered= drivers.loc[drivers['Driver']==driver_choice].reset_index() #TODO #360 the passed object has to select from columns verus rows

    label_dict = utils.get_label_dict(drivers)
    format_dict  = utils.get_format_dict(drivers)
    metric_format_dict  = utils.get_metric_dict(drivers)



    # driver_filtered= drivers.drivers.column==driver_choice.reset_index()
    # driver_filtered= drivers.loc[drivers['Driver']==driver_choice].reset_index()
    # driverFiltered.to_csv('CheckThis.csv')

    # print("FROM SFT 49:driverFiltered\n",driver_filtered)
    # 5. Filter DriversFile by #4

    if driver_label == None:
        target_driver = label_dict.get(driver_filtered.Driver.iloc[0])  # Replaces driver_filtered.Driver.iloc[0]
        posted_drivers = drivers_file.loc[drivers_file['Driver'] == driver_filtered.Driver.iloc[0]] #if isinstance(drivers_file, pd.DataFrame) else drivers_file
        # posted_drivers.to_csv('PostedDrivers.csv')
    else:
        target_driver = driver_label  # Sets target_driver to the driver label if one is given
        posted_drivers = drivers_file.loc[drivers_file['Driver']== driver_filtered.Driver.iloc[0]]
    # print(f'{target_driver=}')
    print("FROM SFT:POSTED DRIVERS\n",posted_drivers)

    # 6. Filter Numerators by #4
    target_num = driver_filtered.Metric[0]
    try:

        posted_num = nums_file.loc[nums_file['variable']== target_num]# TODO #359 change to Numerator in Drive_X

    except:
        posted_num = nums_file.loc[nums_file['Numerator']== target_num]#change to Numerator in Drive_X
    # 7. Filter Denominators by #4
    target_denom = driver_filtered.Denominator[0]
    #change Next Line to Numerator in Drive_X
    try:
        posted_denom = nums_file.loc[nums_file['variable']== target_denom]
    except:
        posted_denom = nums_file.loc[nums_file['Denominator']== target_denom]
    if attributes is not None:
        print(attributes)
        # posted_denom['Attribute'] = posted_denom[attributes]


    driverformat = format_dict.get(driver_filtered.Driver.iloc[0])
    metricformat = []
    for i in driver_filtered.Driver.iloc[0].split("/"):
        metricformat.append(metric_format_dict.get(i))

    #likely can drop the postedNum and postedDenom

    return driver_parent, target_driver, target_num, target_denom, posted_drivers, posted_num, posted_denom, driverformat, metricformat



def get_SingleFactor(drivers_file,nums_file,denoms_file, drivers, driver_choice = None, attributes = None, driver_label = None):

    """ Gets the single factor Drivers """
    
    # TODO  #362 Convert to method 
    # TODO #364 Create conditional to run either using given drivers_holding or an existing dataframe

    if isinstance(drivers, pd.DataFrame):
        driver_parent, target_driver,target_num,target_denom, posted_drivers, posted_num, posted_denom, driverformat, metricformat = singlefactor_df(drivers_file,nums_file,denoms_file,drivers, driver_choice, attributes, driver_label)
        print('This is a dataframe for drivers')
        return driver_parent, target_driver,target_num,target_denom, posted_drivers, posted_num, posted_denom, driverformat, metricformat
    else:

        driver_parent, target_driver,target_num,target_denom, posted_drivers, posted_num, posted_denom = singlefactor_list(drivers_file,nums_file,denoms_file, drivers, driver_choice, attributes, driver_label)
        print('This is NOT a dataframe for drivers')
        return driver_parent, target_driver, target_num, target_denom, posted_drivers, posted_num, posted_denom
