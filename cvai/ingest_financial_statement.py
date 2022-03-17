import os
import pandas as pd

#from tkinter import filedialog as tk

import re

try:
    import ingest_local_textdata as ilt
except ImportError:
    from cvai import ingest_local_textdata as ilt
    
def load_financials_from_folder(targetdir):
    ''' 
    Takes files from a folder and adds them to a dictionary of dataframes.  Likely can be transfered to the ingestion manager.
    
    '''
    import os
    import pandas as pd
    
    # targetsheet = "Historical Financial" #sets the sheetname
    x = os.listdir(targetdir) #get list of files 
    files = [f for f in x if(f[-3:] == 'txt')] #filters to only Excel files
    df = pd.DataFrame()  #initializies a dataframe
    frames_dict = {}
    
    
    for f in files:
        data = pd.read_csv(os.path.join(targetdir,f), header=8, skiprows=1 ,sep=",", skip_blank_lines=True, mangle_dupe_cols=True, quotechar='"', encoding='utf-8') 
        #can this be setup as a method and passed based on a file type or folder name?
        
        data = change_unnamed_cols(data)
        data, month_cols = add_years_to_month(data,f)
       #TODO #170 Create a method for ingestion required treatments versus encapsulation treatments 
        # df, date_cols= set_date_columns(data) 
        data = data.drop(['section'], axis=1) # is this a cleaning step or ingestions step?
        data = data.set_index(['account']).T #this trasnposes the data - can this be flagged in config file?
        data = data.rename_axis('Date').reset_index()
        data['source'] = f
        data['Date'] = pd.to_datetime(data.Date, format='%B %Y') 
        
        frames_dict[f] = data
        # print('*****file:\n',f,' loaded')
    
    return frames_dict

def change_unnamed_cols(data):
    ''' 
    Sweeps and changes unnamed columns
    '''
    unnamed_cols = [col for col in data.columns if 'Unnamed:' in col]
    data = data if not unnamed_cols else data.rename(columns={unnamed_cols[0]:'section',unnamed_cols[1]:'account'})
    return data

def add_years_to_month(data,f):
    ''' 
    Adds years to months when dates don't include
    '''
    file_year =str(re.search(r'\d{4}',f).group(0))
    month_cols = [col for col in data.columns if not col in ['section','account', 'source', 'Total']]
    for col in data.columns:
        if col in month_cols:
            data = clean_currency(data,col)
            data = data.rename(columns={col:col+" "+str(file_year)})
        if col == 'Total':
            data = data.drop(col, axis=1)
    month_cols_new =  [col for col in data.columns if not col in ['section','account', 'source']]        
    
    return data, month_cols_new


def clean_currency(data,col):
    data[col] = data[col].astype(str)
    data[col] = data[col].map(
            lambda x: x.strip(')').replace('(', '-'))
    data[col] = data[col].replace({'\$': '', ',': ''}, regex=True).astype(float)
    # print(f,col, data[col].apply(type).value_counts())
    return data



# targetdir = tk.askdirectory()
# frames_dict = load_financials_from_folder(targetdir)
# frame_dict_2 = ilt.load_dictionary_from_folder(targetdir)
# frames_dict3 = {**frames_dict,**frame_dict_2}
# # print("FRAMES:\n",(frames_dict3))

# df =ilt.unpack_dictionary(frames_dict3)
# #df.to_csv('ptplus_test.csv')
