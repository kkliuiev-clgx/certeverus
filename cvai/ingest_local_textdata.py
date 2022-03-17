import os
import pandas as pd


def load_dictionary_from_folder(targetdir):
    ''' 
    Takes files from a folder and adds them to a dictionary of dataframes.  Likely can be transfered to the ingestion manager.
    
    '''
    import os
    import pandas as pd
    
    # targetsheet = "Historical Financial" #sets the sheetname
    x = os.listdir(targetdir) #get list of files 
    files = [f for f in x if(f[-3:] == 'csv')] #filters to only Excel files
    df = pd.DataFrame()  #initializies a dataframe
    frames_dict = {}

    
    for f in files:
        data = pd.read_csv(os.path.join(targetdir,f))
        data['source'] = f
        df, date_cols= set_date_columns(data)
        # print('*****COLUMNS:\n',f," has ",df.columns, "and", date_cols)
        frames_dict[f] = df
    
    return frames_dict


def set_date_columns(data):
    ''' 
    Sweeps files to replace current date-related columns
    '''
    date_cols = [col for col in data.columns if 'DATE' in col[-4:]]
    data = data if not date_cols else data.rename(columns={date_cols[0]:'Date'})
    return data, date_cols


def unpack_dictionary(frames_dict):
    '''
    Create a single Concated DataFrame from each of the Frames Dictionary Values
    '''
    mdfmerged = pd.DataFrame()

    for k,v in frames_dict.items(): # loop to step through each key value pair of frame dictionary
        v['Date'] = pd.to_datetime(v['Date']) if 'Date' in v.columns else "2021-06-30"
        v =v.set_index('Date') 
        mdfmerged =  pd.concat([mdfmerged,v], sort=False, ignore_index=False)#concatenates the frames
        mdfmerged.to_csv("accordian_data.csv")
        # mdfmerged['Scenario'] = mdfmerged['Sourced']
    df = mdfmerged
    return df









# Main Function working area

# targetdir = tk.askdirectory()
# frames_dict = load_dictionary_from_folder(targetdir)
# df =unpack_dictionary(frames_dict)
# df.to_csv('ptplus_test.csv')
# # print(frames_dict)
# print(df, df.info())



