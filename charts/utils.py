
import inspect
from cvai.filter_manager import filter_drivers
import logging

import pandas as pd
import plotly
import simplejson as json
from cvai import PlotIsoquant as pi
from cvai import PlotWaterfall as pwf

from cvai import transformation_manager as tm
from cvai import sparklineTransformation as st
from cvai import Waterfall_Transformation as wt
from cvai import singleFactorTransformation as sf
from cvai import PlotSingleFactor as psf
from cvai import plot_table as pt
from cvai import derivatives as dv
from cvai import plotNodeMap as pnm
from cvai import plot_dashboard as td
from django.db import connection

from core.utils import get_engine


logger = logging.getLogger(__name__)


def get_parent_items(client):

    items = []
    try:
        cursor = connection.cursor()

        query = "SELECT DISTINCT(\"Parent\") FROM %s" % client.get_drivers_table_name(
        )
        cursor.execute(query)
        records = cursor.fetchall()
        print(records)
        for row in records:
            if row[0]:
                items.append(row[0])
        cursor.close()

    except:
        logger.exception("Failed to get parent items")
    finally:
        if connection:
            connection.close()
    print(items)
    return items


def get_driver_items(client):

    items = []
    try:
        cursor = connection.cursor()

        query = "SELECT \"Parent\", \"Driver\", \"Attributes\" FROM %s ORDER BY \"Order\"" % client.get_drivers_table_name()
        cursor.execute(query)
        records = cursor.fetchall()
        # print(f'{records=}')
        logger.exception(
            f" {inspect.getframeinfo(inspect.currentframe()).function}:{inspect.getframeinfo(inspect.currentframe()).lineno} : Printed from get_driver_items")
        for row in records:
            items.append(
                {
                    "parent": row[0],
                    "driver": row[1],
                    # TODO: [CAM-43] THis should be replaced with the label name for the use in drop
                    "attrib": row[2]
                }
            )
        cursor.close()

    except:
        logger.exception("Failed to get parent items")
    finally:
        if connection:
            connection.close()
    print("Drivers itesm are here:", items)
    return items


def get_attrib_items(client):

    items = []
    try:
        cursor = connection.cursor()

        query = "SELECT \"Driver\", \"Attributes\" FROM %s" % client.get_drivers_table_name()
        cursor.execute(query)
        records = cursor.fetchall()
        print("ATTRIBS>>>>>>>\n", records)
        for row in records:
            if row[1] is not None:
                attriblist = row[1].split(',')
                for attrib in attriblist:
                    items.append(
                        {
                            "driver": row[0],
                            "attribs": attrib
                        }
                    )

        cursor.close()

    except:
        logger.exception("Failed to get attrib items")
    finally:
        if connection:
            connection.close()
    print(items)
    return items


def get_filter_items(client):
    """ This gets the filter list for flitering"""
    items = []
    print('CLIENT NAME IN FILTER ITEMS:', client.name)
    try:
        cursor = connection.cursor()
        if client.name.strip() in ['Accordion_inv', 'Accordion_source', 'SalesDemo2', 'Alloy_Scale', 'Channel_Mgr']:
            filter_target = {'Accordion_inv': 'Commodity', 'Accordion_source': 'Name_Vendor',
                             'Alloy_Scale': 'Branch', 'SalesDemo2': 'CAE', 'Channel_Mgr': 'Channel AE'}
            print('SUCCESS for %s' % client.name,
                  filter_target.get(client.name.strip()))
            query = "SELECT DISTINCT \"%s\" FROM %s ORDER BY \"%s\"" % (filter_target.get(
                client.name.strip()), client.get_dfclean_table_name(), filter_target.get(client.name.strip()))
            # print(f'{query}')

        else:
            print('FAIL')
            logger.exception("Failed to get Filter items")

        # query = "SELECT DISTINCT\"Commodity\" FROM %s" % client.get_dfclean_table_name()
        cursor.execute(query)
        records = cursor.fetchall()
        print("RECORDS>>>>>>>\n", records)  # TESTING
        for row in records:
            if row[0]:
                items.append(
                    {
                        "filtered_by": row[0]
                    }
                )
        cursor.close()
        # print('FILTERS', filter_by)

    except:
        logger.exception("Failed to get Filter items")
    finally:
        if connection:
            connection.close()
    # print(f'at {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} >>>>ITEMS:\n', items)
    return items


def get_label_items(client):

    items = []
    try:
        cursor = connection.cursor()

        query = "SELECT \"Driver\", \"Label\" FROM %s" % client.get_drivers_table_name()
        cursor.execute(query)
        records = cursor.fetchall()
        for row in records:
            items.append(
                {
                    "driver": row[0],
                    "label": row[1]
                }
            )
        cursor.close()

    except:
        logger.exception("Failed to get label items")
    finally:
        if connection:
            connection.close()
    return items


def get_chart_data(client, params):
    # NOTE: The code below should mimic cvai/server.py

    engine = get_engine()
    chart_type = params.get("chart_type")

    parent = params.get("parent")
    start_date = params.get("start_date")
    end_date = params.get("end_date")
    resample_period = params.get("resample_period")
    driver = params.get("driver")
    is_sorted = params.get("ordered", "false") == "true"
    pva = params.get("pva", "true") == "false"
    ytd = params.get("ytd", "false") == "true"
    # filtered_by = None #Used for testing REMOVE FOR PRODUCTION
    filtered_by = params.get("filtered_by")
    # print(f'At {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} ytd value:',
    #   ytd, "pva:", pva, "sorted:", is_sorted, "filtered_by:", filtered_by)
    #aggdata = params.get("aggdata", "false") == "true"
    attribs = params.get("attribs")

    # GET DATAFRAMES

    drivers = pd.read_sql_table(
        client.get_drivers_table_name(), engine, parse_dates=True)  # TODO: [CAM-45] Adjust Isoquant Chart Title to include x label
    df = pd.read_sql_table(client.get_dfclean_table_name(),
                           engine, parse_dates=True, index_col='Date')
    # print(f'FROM {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} INITIAL DF', df, '\n\n')
    drivertest = pd.read_sql_query("""SELECT * 
                                    FROM """ + client.get_drivers_table_name()+""" 
                                    WHERE "Parent" = '"""+parent+"""' 
                                    ;
                                    """, engine)
    num = tuple(drivertest['Metric'].to_list(
    ))  # TODO #261 We should consider filtering more explicitly to include the any date start/end points right from the SQL

    # dftest = pd.read_sql_query("""SELECT """+{}+"""
    #                                 FROM """ +client.get_dfclean_table_name()+""" ;
    #                                 """.format(num),engine)

    #print('DFTEST:\n',drivertest, num,"\nAttribs:\n", attribs, "\nAgg Data:\n",aggdata)
    # print(f' At {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno}Client:', client.name.strip(), "!")

    if client.name.strip() == 'FHMS':

        print('This is for FHMS - positive test with ', attribs)
        DriversFile, NumsFile, DenomsFile = tm.CreateDrivers(
            drivers, df, parent, resample_period, attribs, start_date, end_date, ytd)

    else:
        if attribs is None:
            attribute_list = ['Scenario']
        else:
            attribute_list = ['Scenario', attribs]
        # print(f'at {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} {attribute_list=}')

        filter_dict = {'Accordion_inv': 'Commodity', 'Accordion_source': 'Name_Vendor',  'Alloy_Scale': 'Branch', 'SalesDemo2': 'CAE',
                       'Channel_Mgr': 'Channel AE'}  # TODO The user should see this filter created dynamically and controlled by the config file

        if client.name.strip() in ['Accordion_inv', 'Accordion_source', 'Alloy_Scale', 'SalesDemo2', 'Channel_Mgr']:
            filt = filter_dict.get(client.name.strip())
            df = df[df[filt] == filtered_by] if filtered_by is not None else df
        # elif client.name.strip() == 'SalesDemo2':
        #     df = df[df['CAE']==filtered_by] if filtered_by is not None else df
        else:
            df = df[df.Name_Vendor ==
                    filtered_by] if filtered_by is not None else df

        print(f"FROM {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} \n", df, filtered_by)

        DriversFile, NumsFile, DenomsFile = tm.create_drivers(
            df, drivers, parent, resample_period, attribute_list, start_date, end_date, ytd)
        # print(f' At {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno}:This is for ', client, 'with', attribs)
        # print(f"FROM{inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno} DRIVERS FILE *****************************************************************\n", DriversFile)

    # OBJECT METHOD SHOULD BE BETWEEN GET DATAFRAMES AND HERE

    # label = driver_dict.get(driver)

    if chart_type == "waterfall":

        DriversSorted = wt.FilterSOCdates(
            DriversFile, start_date, end_date, pva)
        # print("\n\n@@@@@@@@@@ from UTILS\n", DriversSorted,"\nUTILS GCD @@@@@@@@@@@@@\n")
        # print("wt", wt, client
        # print(pwf.plotWaterfall(
        #         wt.get_waterfall(DriversSorted, is_sorted, parent),parent
        #     ))

        return plotly.io.to_json(
            pwf.plotWaterfall(
                wt.get_waterfall(DriversSorted, drivers, is_sorted,
                                 parent, pva), parent, pva, end_date, drivers)
        )

    if chart_type == "isoquant":
        # print(" from utils174 DRIVER:", driver)
        # print(" from utils175 ATTRIBS:", attribs)

        driverParent, targetDriver, targetNum, targetDenom, postedDrivers, postedNum, postedDenom, driverformat, metricformat = sf.get_SingleFactor(
            DriversFile, NumsFile, DenomsFile, drivers, driver, attribs)

        # print("posteddrivers from utils 243:\n", postedDrivers, "\nposted denom:\n",
        #   postedDenom)  # TODO #239 Add Attribute to postedDenom
        print("pi", client, attribs)
        # print(
        #     pi.plotisoquant(
        #         driverParent, targetDriver,targetNum,targetDenom, postedDrivers, postedNum, postedDenom,attribs, ytd
        #         )
        #     )
        return plotly.io.to_json(
            pi.plotisoquant(
                driverParent, targetDriver, targetNum, targetDenom, postedDrivers, postedNum, postedDenom, attribs, ytd, driverformat, metricformat
            )
        )

    if chart_type == "sparkline":
        print("st", st, client)
        # print(st.Sparkline(DriversFile))
        return plotly.io.to_json(
            st.Sparkline(DriversFile, drivers)
        )

    if chart_type == "single_factor":

        driverParent, targetDriver, targetNum, targetDenom, postedDrivers, postedNum, postedDenom, driverformat, metricformat = sf.get_SingleFactor(
            DriversFile, NumsFile, DenomsFile, drivers, driver)

        print("psf", psf, client)

        return plotly.io.to_json(
            psf.plotSingleFactor(
                driverParent, targetDriver,
                targetNum, targetDenom,
                postedDrivers, postedNum,
                postedDenom, driverformat, metricformat
            )
        )

    if chart_type == "nodemap":

        # print("JJJJJJJJJJJJJJJJJJ ", NumsFile)
        return plotly.io.to_json(
            pnm.createMap(NumsFile, parent)
        )

    if chart_type == "prescriptions":

        # sDriversFile, sNumsFile, sDenomsFile = tm.create_drivers(
        #     df, drivers, parent, resample_period, 'CAE', start_date, end_date, True)
        # sdriverParent, stargetDriver, stargetNum, stargetDenom, spostedDrivers, spostedNum, spostedDenom = sf.get_SingleFactor(
        #     sDriversFile, sNumsFile, sDenomsFile, drivers, driver)

        # print(f'This is {spostedNum=}'+'*************$$$$$$$')

        nodes = pnm.createMap(NumsFile, parent, chart_type)

        try:
            pva = True
            DriversSorted = wt.FilterSOCdates(
                DriversFile, start_date, end_date, pva)
            waterfallpva = pwf.plotWaterfall(
                wt.get_waterfall(DriversSorted, drivers, is_sorted,
                                 parent, pva), parent, pva, end_date, drivers
            )
        except:
            waterfallpva = None

        pva = False

        DriversSorted = wt.FilterSOCdates(
            DriversFile, start_date, end_date, pva)
        waterfall_time = pwf.plotWaterfall(
            wt.get_waterfall(DriversSorted, drivers, is_sorted, parent,
                             pva,), parent, pva, end_date, drivers
        )
        # Develops a test set for plotting

        actions_table = dv.main()   

        fig = td.create_product_page(
            waterfallpva, waterfall_time, actions_table, nodes)

        print(plotly.io.to_json(fig))
        return plotly.io.to_json(fig)
# Functions below are used to create each dictionary wherever it is needed #


def get_label_dict(drivers):
    label_dict = {}
    for i in range(len(drivers)):
        # Creates dictionary of driver-label pairs
        label_dict.update({drivers['Driver'][i]: drivers['Label'][i]})
    return label_dict


def get_format_dict(drivers):
    format_dict = {}
    for i in range(len(drivers)):
        # Creates dictionary of driver-format pairs
        format_dict.update({drivers['Driver'][i]: drivers['Format'][i]})
    return format_dict


def get_metric_dict(drivers):
    metric_format_dict = {}
    for i in range(len(drivers)):
        # Creates dictionary of metric-format pairs
        metric_format_dict.update(
            {drivers['Metric'][i]: drivers['Metric Format'][i]})
    return metric_format_dict
