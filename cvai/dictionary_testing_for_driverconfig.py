'''
This creates a dictionary for aggregation

POSSIBLE TO COMBINE WITH CPT ?
'''

import pandas as pd
# import os

def get_aggregation_dictionary(driver_file):
    ''' This method gets the aggregations into a dictionary for use in calculations'''
    d_frame = driver_file #read drivers file - can be read from SQL/postgres
    #can d_frame come directly from the drivers file?
    dict_agg = d_frame.set_index('Metric').to_dict()['Numerator Type']
    return dict_agg
