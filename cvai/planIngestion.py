import os
import pandas as pd
from datetime import datetime as dt

def Load_Data_from_folder_for_OPX(targetdir, **kwargs):
    targetsheet = "DATA" #sets the sheetname
    df = pd.DataFrame()  #initializies a dataframe
    client = kwargs.get("client")
    if client:
        print('Client for Plan Data is: ',client, client.name.strip())
        files = client.get_files("plan")

        for client_file in files:
            file = client_file.file
            file_name, ext = client_file.get_file_info()
            if ext == "csv":
                client.ingestion_status = "error"
                client.save()
                client_file.ingestion_status = "error"
                client_file.ingestion_error = "The CSV file type is not supported yet"
                client_file.save()

                raise NotImplementedError
            elif ext in ["xls", "xlsx"]:
                if client.get_storage_backend() == "file":
                    data = pd.read_excel(
                        open(file.path, 'rb'),
                        sheet_name=targetsheet,
                        skiprows=1,
                        header=1
                    )
                    name = pd.read_excel(
                        open(file.path, 'rb'),
                        sheet_name=targetsheet,
                        usecols=[0],
                        index_col=None,
                        header=0,
                        nrows=0
                    )
                elif client.get_storage_backend() == "s3":

                    import s3fs
                    from django.conf import settings
                    s3 = s3fs.S3FileSystem(
                        anon=False,
                        key=settings.AWS_ACCESS_KEY_ID,
                        secret=settings.AWS_SECRET_ACCESS_KEY
                    )
                    s3_url = f"{file.storage.bucket_name}/{file.name}"
                    data = pd.read_excel(
                        s3.open(s3_url),
                        sheet_name=targetsheet,
                        skiprows=1,
                        header=1
                    )
                    name = pd.read_excel(
                        s3.open(s3_url),
                        sheet_name=targetsheet,
                        usecols=[0],
                        index_col=None,
                        header=0,
                        nrows=0
                    )

                name = name.columns.values[0] #cleans the name as a variable
                if client.name.strip() == 'FHMS':
                    print('FHMS Melted: ',name)
                    data = pd.melt(data, id_vars=(['Metrics','Name']), var_name="Date") #TODO #256 Plan Data for Non-FHMS clients should not be melted git stats
                    data.value= pd.to_numeric(data.value, errors='coerce')
                    data = data.rename(columns={'Metrics':'variable'})
                    print(data.columns)
                else:
                    print("NOT FHMS")
                    data = data.set_index('Metrics').T
                    data.index = data.index.rename('Date')
                    data = data.reset_index()
                    print(client," transposed")
                    print(data)
                    #data.to_csv("plan_transposed.csv")
                data['Date']= pd.to_datetime(data['Date'], format ='%b%y').dt.normalize()
                data['Name'] = name  #assigns name column
                data = data.dropna() #drops NA
                df = df.append(data, sort = False) #adds plan data to dataframe
                df = df.set_index('Date')
                df = df.rename(columns={'Name' : 'Scenario'}) #renames
            # Update ingestion status
            client_file.ingestion_status = "processed"
            client_file.save()
            # print("PLAN:\n",df)
        return df

    x = os.listdir(targetdir) #get list of files
    files_xls = [f for f in x if f[-4:] == 'xlsx'] #filters to only Excel files

    for f in files_xls:
        data = pd.read_excel(targetdir+f,sheet_name = targetsheet,skiprows =1, header=1)
        name = pd.read_excel(
            targetdir+f,sheet_name = targetsheet, usecols=[0],index_col=None,header = 0, nrows=0
            )
        name = name.columns.values[0] #cleans the name as a variable
        data['Name'] = name  #assigns name column
    #            data = data.rename(columns={"Fiscal Period":"Metric"}) #cleans names
        data = pd.melt(data,id_vars=(['Metrics','Name']), var_name="Date") #Unpivots data
        data.value= pd.to_numeric(data.value, errors='coerce') #converts values to numeric
    #             data.Date = data.Date.str.strip('.1') #cleans date
        data['Date']= pd.to_datetime(data['Date'], format ='%b%y') #converts Date to date time
        data = data.dropna() #drops NA
        df = df.append(data, sort = False) #adds plan data to dataframe
        df = df.set_index('Date')
        df = df.rename(columns={'Name' : 'Scenario', 'Metrics':'variable'}) #renames
        print(name,'loaded') # notify scenario loaded
        #df.to_csv('plan.csv')
    return df
