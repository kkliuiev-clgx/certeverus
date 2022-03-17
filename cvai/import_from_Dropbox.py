import dropbox
import pandas as pd
from contextlib import closing # this will correctly close the request
import io

token = "Si2kikU8Lu8AAAAAAAAAAYJkTGm90CtD54N3x3VhJpOwBwnA8Rtu3OkHPCyQYvVe" 


def read_from_Dropbox_folder(token="Si2kikU8Lu8AAAAAAAAAAYJkTGm90CtD54N3x3VhJpOwBwnA8Rtu3OkHPCyQYvVe"):
    ''' This method extracts a list of files from Dropbox (it matches the readFromFolder method in gdsingestion'''
    dbx = dropbox.Dropbox(token)
    # print(dbx.users_get_current_account(),'\n\n\n')
    filelist = list()
    for entry in dbx.files_list_folder('').entries:
        # print(f'{entry.name=}\n')#, entry,'\n\n\n')
        filelist.append(entry.path_display);print(entry.name)
    # print(f'{filelist =}')
    return filelist

def get_dropbox_file_contents(path):
    ''' 1st path method to get contents of files -  not a direct match for GDSingestion '''
    a,res=dbx.files_download(path)
    with closing(res) as result:
        byte_data=result.content
        return io.BytesIO(byte_data)


def LoadDict(filelist):
    '''
    Load Frames Dictionary with Dropbox DataFrames
    '''
    frames_dict = {}
    mdfmerged = pd.DataFrame()
    for i in filelist: # step through each key value pair and develop an entry for each sheet
        data = get_dropbox_file_contents(i) # DIFFERS HERE FROM GDSIngestion
        frames_dict[i] = data
    return frames_dict



def dropbox_loader(token):
    ''' '''
    flist = read_from_Dropbox_folder(token)
    dbx = dropbox.Dropbox(token)
    yourpath = ('/'+flist[2])
    file_stream=LoadDict(flist)
    # df = pd.read_csv(file_stream)  # need to add a variable type for xlsx, csv, txt, etc
    # print(f'{file_stream =}')

    # NEEDS TO UNPACK
    return

# Use Locally 

dbx = dropbox.Dropbox(token)
dropbox_loader(token)

