class Load():  #needs help content
    
    '''Step 1.1A: Load the Financial Data from Guru Focus and return a dataframe'''
    def LoadGuruFocus():
        import pandas as pd
        import numpy as np
        import urllib.request, json
        from pandas.io.json import json_normalize
        import collections
        import csv




        def load_metrics(): # Read the filtering file based on the variables needed for the analysis
            ''' This is the function to load the metrics for the analysis'''
            
            with open('sva\Testing_Dictionary.csv', mode='r', encoding='utf-8-sig') as f:  #reads the file
                reader = csv.reader(f) #reads
                mets = tuple(reader)   # creates a tuple

            return mets




        def load_peer_file(companyfile):   # function to get the company list
            ''' This is the function to load the peers for the analysis'''
            peerset= pd.read_csv(companyfile) # load a dataframe
            companyset = peerset.Peers.unique() # get unique values for each company
            return companyset


        

        def load_API(name):    
            ''' This is the function to load the dictionary from the API'''
            # Sets the URL for Financials (will do same for stock prices and dividends)

            LoadFinancialsURL = 'https://api.gurufocus.com/public/user/c8c4a097da5576a7a3019e1bf96234a4:e5df50b8dcf8d926d541781fee2cf3ef/stock/'+name+'/financials'

            response = urllib.request.urlopen(LoadFinancialsURL) # Loads the data for the company from GF
            content = response.read() # gets JSON file
            data = json.loads(content.decode('utf8'))  # Creates dictionary from JSON
            data = (data['financials']['quarterly'])  # Gets the quaterly financials
            return data




        def flatten(data): # function to parse the json dataset into a single library for unpacking
            ''' This is the function to Flatten the Data '''
            flat = {} # create empty library
            for k, v in data.items(): # iterate over the key values and items
                if isinstance(v, dict):             # 
                    for j, u in flatten(v).items():
                        flat[k+'-'+j] = u
                else:
                    flat[k] = v
            return flat

       
        ''' This is the function for loading the data from API, flatten the dictionary, create a dataframe, 
        and combining them into a dataframe with the company name attatched
        '''
        def Load_Data(companyset):
            df = pd.DataFrame()
            for name in companyset:

                data = load_API(name)
                # This flattens the original dictionary and then filters on the metrics we wish to keep taken from a CSV file set for the analysis

                data2 = flatten(data) # call function to parse the dictionary 
                data2a = dict((k, data2[k]) for k in mets[0] if k in data2) # filter the dictionary based on the filter

                #print('This is company',name,'started')

                df1 = pd.DataFrame(data2a) # Creates a dataframe from the filtered dictionary

                columnheaders = df1.columns[1:]  #Creates a variable for the columnheaders

                df1 = df1.melt(id_vars = ['Fiscal Year'], value_vars =(columnheaders)) # Melts the dataframe
                df1['Name'] = name # Applies the company name to the dataframe


                #print(df1.head(5))
                print(name,'loaded')

                df = df.append(df1, sort = False)

            return df

        ''' This is the function for splitting the name and source from dataframe'''
        
        def Clean_data(df):       
            ''' This is the function for splitting the name and source from dataframe'''        
            new = df["variable"].str.split("-", n = 1, expand = True) # Splits the Variable 

            # making separate source column from new data frame 
            df["Source"]= new[0] 
            # making separate metric column from new data frame 
            df["Metric"]= new[1] 
            # drop the original dictionary column
            df.drop(columns =['variable'], inplace = True)
            df['Fiscal Year']= pd.to_datetime(df['Fiscal Year']) #converts Date to date time
            df = df.astype({'value':'float64'})
            df = df[['Metric','Name','Fiscal Year','value','Source']]
            df.rename(columns={'Fiscal Year':'Date'}, inplace=True)
            return df

        df = pd.DataFrame()
        mets = load_metrics()
        companyset = load_peer_file('sva\Company Targets.csv') #may neeed to be made to a user input variable
        df = Load_Data(companyset)    
        df = Clean_data(df)
        return df


    '''Step 1.1B: Load the Financial Data from a folder and return a dataframe'''

    ''' This is the function for loading the data from multiple xlxs files in a folder and combining them into a dataframe''' 
    # Needs to be retested - peer files are defined by the folder contents
    # Still missing TTM and source data

    def Load_Data_from_folder(targetdir):
        import os
        import pandas as pd

        #targetdir = "d:/DigX Solutions/Certe Verus - Product Dev - General/ACN Data/" #sets the target directory in the event it is not passed
        #target = targetdir+"Pure Storage Stock_Dataset_GuruFocus_2019-10-25-08-48.xlsx" #sets the file
        targetsheet = "Historical Financial" #sets the sheetname

        x = os.listdir(targetdir) #get list of files 
        files_xls = [f for f in x if f[-4:] == 'xlsx'] #filters to only Excel files

        df = pd.DataFrame()  #initializies a dataframe

        for f in files_xls:
            data = pd.read_excel(targetdir+f,sheet_name = targetsheet,skiprows =1, header=1, usecols = "A,EI:EW")# builds the dataframe
            name = pd.read_excel(targetdir+f,sheet_name = targetsheet, usecols=[0],index_col=None,header = 0, nrows=0) #gets the name
            name = name.columns.values[0] #cleans the name as a variable
            data['Name'] = name  #assigns name column
            data = data.rename(columns={"Fiscal Period":"Metric"}) #cleans names
            data = pd.melt(data,id_vars=(['Metric','Name']), var_name="Date") #Unpivots data
            data.value= pd.to_numeric(data.value, errors='coerce') #converts values to numeric
            data.Date = data.Date.str.strip('.1') #cleans date
            data['Date']= pd.to_datetime(data['Date'], format ='%b%y') #converts Date to date time
            data.loc[:,:]=data.loc[:,'value'].dropna()



            df = df.append(data, sort = False) 

        return df # returns dataframe for analysis


    '''Step 1.2: Apply the Drivers and return a dataframe'''

    def Apply_Drivers(df,Driverloc):

        import pandas as pd #import pandas to work on dataframes

    #     drivers = pd.DataFrame({"Metric":['Operating Income','Revenue','Total Assets'],'Denominator':['Revenue','Total Assets','1'],'Driver' : ['EBIT/Revenue','Revenue/Total Assets','Total Assets']}) # builds dataframe and assigns Drivers for the join NB: This will have to be imported from another file likely a CSV or Excel file

        drivers = pd.read_csv(Driverloc) #assigns the drivers from the target csv file
        df = pd.merge(df,drivers,on='Metric') # Joins Dataframe with Drivers File on Metric
        df = df.dropna()

        return df #returns a revised data frame that is filtered for the drivers

    ''' Step 1.3 -  Load the drivers'''

    def Lock_and_Load1(targetdir,Driverloc):
        import SVA3 as BOOM
        import pandas as pd
        import numpy as np
        df = BOOM.Load_Data_from_folder(targetdir) 
        df2 = BOOM.Apply_Drivers(df,Driverloc)
        return df2


    ''' Step 1.4 Fill denominators '''

    def Fill_Denom_value(df2):
        import SVA3 as BOOM
        import pandas as pd
        import numpy as np

        df2.rename(columns = {'Metric':'Numerator'}, inplace = True) # renames the column metric to numerator for use in the function
        df_denom = df2.copy(deep=False) # Provides a copy of the dataframe to use for lookup
        df_num= df2.copy(deep=False) # Provides a copy of the dataframe to use for lookup
        df_denom["Key"] = df_denom['Denominator'] # sets the new column 
        df_num["Key"] = df_num['Numerator'] # sets the new column 

        df_num.set_index(['Name','Date', 'Key']) # sets the indices for the the numerator df
        df_denom.set_index(['Name','Date', 'Key']) # sets the indices for the the numerator df

        merged_df = df_denom.merge(df_num, on = ['Name','Date','Key'], how = 'left',suffixes =['','_D']) # merges the Dataframes on Key
        merged_df = merged_df.drop(columns =['Driver_D','Denominator_D','Order_D','Parent_D','Level_D','Numerator_D'])# Cleans up a few of the columns
        merged_df = merged_df.fillna(1) # fills the Null Values with 1 as the denominators
        return (merged_df)

    ''' Step 1.5 Apply filter and Dictionary '''   
   

    def filterdate(merged_df): #Function to filter down dates
        import pandas as pd # Import Pandas
        ts = merged_df['Date'].max() # Find Max Date in data set
        a = str(ts.year-4)+'/'+str(ts.month)+'/'+str(1) # subtract 4 years
        startdate = pd.to_datetime(a) #Get the time stamp for filtering set
        fmerged_df = merged_df.loc[merged_df['Date']> startdate,:] # Create the new dataset
        return fmerged_df
    
    def apply_ttm(fmerged_df): #function to create the dictionary
        import pandas as pd
        a =list(fmerged_df.Source.unique()) #getting the list of unique sources
        dict1 = {k:('TTM' if k =='income_statement' or k== 'cashflow_statement' else 'End') for k in a} # populating the dictionary
        return dict1
    
  
    ''' Step 1.6 Apply Dictionary to Sources ''' 
    
    def ttm_source(fmerged_df,TTM_dictionary):
        import pandas as pd
        fmerged_df= fmerged_df.reset_index(drop=True) #Resets the index
        fmerged_df.loc[:,'NumTTM']=fmerged_df.loc[:,'Source'].map(TTM_dictionary) #maps the dictionary to the Sources
        fmerged_df.loc[:,'DenTTM']=fmerged_df.loc[:,'Source_D'].map(TTM_dictionary) #maps the dictionary to the Source_D
        return fmerged_df


    
    
    def Lock_and_Load(Driverloc,dataf):
        import pandas as pd
        import SVA3 as BOOM

        #Step 2 - Apply the drivers
        dfd = BOOM.Load.Apply_Drivers(dataf,Driverloc)

        #Step 3 - Apply Denominators
        merged_df = BOOM.Load.Fill_Denom_value(dfd)

        #Step 4 - Filter the Data by Date
        fmerged_df= BOOM.Load.filterdate(merged_df)

        # Step 5 - Create TTM dictionary
        TTM_dictionary = BOOM.Load.apply_ttm(fmerged_df)
        #TTM_dictionary

        # Step 6 - Apply the TTM dictionary to the numerators and denominators
        fmerged_df = BOOM.Load.ttm_source(fmerged_df,TTM_dictionary)
        return fmerged_df
    
    ''' 
    LOAD CLASS ENDS HERE
    
    '''
    
    
class Filter():
    
    def Target(fmerged_df,Company,SelDriver): #function to produce a Target dataframe
        ''' This function filters a dataframe based on the target company name.  It can be used with other functions to 
        filter time periods, drivers, Numerators and other attributes
        '''
        Target_df= fmerged_df[(fmerged_df['Name']==Company)&(fmerged_df['Driver']==SelDriver)]
        return Target_df

    def Peer(fmerged_df,Company,SelDriver):#function to produce a Peer dataframe

        ''' This function filters a dataframe based on the peers to a company.  It can be used with other functions to 
        filter time periods, drivers, Numerators and other attributes
        '''

        Peer_df= fmerged_df[(fmerged_df['Name']!=Company)&(fmerged_df['Driver']==SelDriver)]
        return Peer_df

    def Filter_Company(fmerged_df,Company):
    
        ''' This function filters a dataframe based on the target company name.  It can be used with other functions to 
        filter time periods, drivers, Numerators and other attributes
        '''
        ffmerged_df = fmerged_df.loc[(fmerged_df.loc[:,'Name']==Company)&(fmerged_df.loc[:,'Level']!='NONDRIVER')]
        return ffmerged_df

    def Filter_Driver(fmerged_df,SelDriver):

        ''' This function filters a dataframe based on the drivers.  It can be used with other functions to 
        filter time periods, drivers, Numerators and other attributes
        '''   

        ffmerged_df = fmerged_df.loc[(fmerged_df.loc[:,'Driver']==SelDriver)&(fmerged_df.loc[:,'Level']!='NONDRIVER')]
        return ffmerged_df

    def Filter_Peers(fmerged_df,Company):
        ''' This function filters a dataframe based on the drivers.  It can be used with other functions to 
        filter time periods, drivers, Numerators and other attributes
        '''       
        ffmerged_df = fmerged_df.loc[(fmerged_df.loc[:,'Name']!=Company)&(fmerged_df.loc[:,'Level']!='NONDRIVER')]
        return ffmerged_df

    
    ''' 
    FILTER CLASS ENDS HERE
    
    '''    
class Chart():
    
    def SingleFactor(dataset, Company, selection):
        """ This function passes the dataframe, the driver, and the company name to plot a single factor Driver chart
        and the numerator and denomintor charts on 3 subaxes
        """
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        # import seaborn as sns
        from pandas.plotting import register_matplotlib_converters
        register_matplotlib_converters()
        #selection = input("What driver?")

        #selection = 'Net Revenue/Apps'#manual setting of the factor

        #dataset['Date']= str(dataset['Date'])

        seldata = Filter.Filter_Company(Filter.Filter_Driver(dataset,selection),Company)
        #assigns dataset and filters Driver and Company
        gridsize = (3, 2) # sets grid for plot
        fig = plt.figure(figsize=(12, 8)) # sets the size for export
        ax1 = plt.subplot2grid(gridsize, (0, 0), colspan=3, rowspan=2) #sets the first axes
        ax2 = plt.subplot2grid(gridsize, (2, 0)) #sets the subplot for numerator
        ax3 = plt.subplot2grid(gridsize, (2, 1)) # sets the subplot for denominator

        main_title = str(seldata.Name.unique()[0])+'-'+str(selection)
        ax1.set_title(main_title,fontsize=14, loc ='left')
        DriverValue = seldata.value/seldata.value_D
        BarC = ax1.bar(seldata.Date,DriverValue, width = 75)
        ax2.bar(seldata.Date,seldata.value, width = 75)
        ax3.bar(seldata.Date,seldata.value_D, width = 75)
        ax2.set_title(seldata.Numerator.unique()[0], fontsize=14, loc ='left', c ='k')
        ax3.set_title(seldata.Denominator.unique()[0],fontsize=14, loc ='left', c='k')
        name = ("singlefactor "+seldata.Numerator.unique()[0]+".png")
        fig.savefig(name)
        fig.tight_layout()
  #      plt.show()
        return
    
    # This module creates the standard sparkline charts

    def Sparkline(fmerged_df, Company):
        """ This function passes a dataframe and company name to produce the sparklines for each of the drivers 
        in a single axes
        """
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        # import seaborn as sns
        from pandas.plotting import register_matplotlib_converters
        register_matplotlib_converters()

        plt.style.use('seaborn')

        dataset = Filter.Filter_Company(fmerged_df,Company)

        dataset.loc[:,'Date'] = pd.to_datetime(dataset.loc[:,'Date']) #converts the Date to datetime type

        Driverset = tuple(dataset.loc[:,'Driver'].unique()) # gets the unique drivers in the dataset
        plotneed = len(Driverset) #counts the number of drivers to set up the subplot rows
        print("here is the set: ",Driverset) # check  what is passed
        plt.rcParams.update({'figure.autolayout': True})

    #     fig, ax = plt.subplots()

        plt.figure(1)
        fig = plt.figure(figsize=(12,8)) #sets the plot size
        plotnum = 1 #initiates the loop

        for i in Driverset: # For Loop to iterate through the Drivers tuple
            if i == "/": # Checks to see if the Driver is "/" or Blank
                continue # Iterates past Blank Driver

            plt.subplot(plotneed,1,plotnum)
            fildata = dataset.loc[dataset.loc[:,'Driver'] == i] #filters the dataset by driver
    #         print(fildata)
            fildata.loc[:,'DV'] = fildata.loc[:,'value']/(fildata.loc[:,'value_D'])
    #         print("\nNow - for ",i,"\n",  fildata.loc[:,'DV'])
            plt.plot(fildata.loc[:,'Date'],fildata.loc[:,'DV'],"-o", mfc = '#FFFFFF',ms = 10, mew = 2) #Plots 
            plt.title(Company +" - "+ i, loc = 'left', size =14) #Places Title on the LHS
            plt.box(True)

            plotnum = plotnum+ 1 #increments the plot position
    #         years = mdates.YearLocator()   # every year
    #         months = mdates.MonthLocator()  # every month
    #         years_fmt = mdates.DateFormatter('%Y')    

    #         ax.xaxis.set_major_locator(years)
    #         ax.xaxis.set_major_formatter(years_fmt)
    #         ax.xaxis.set_minor_locator(months)
 #       plt.show()
        name = "sparkline -"+Company+".png"
        fig.savefig("sparkline.png",dpi=200,bbox_inches='tight')
        return

    def Isoquant (fmerged_df, SelDriver):
        """This function passes the dataframe and a selected driver and returns a chart for the isoquants
        """

        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt

        # will pass Scenario, Data, 
        # x = dataset[Value]
        # y = dataset[DriverValue]

        # load DataFrame HASHTAG OUT IN POWERBI
        iso_df = Filter.Filter_Driver(fmerged_df,SelDriver)
        iso_df = Calc_DriverValue(iso_df,SelDriver)
        iso_df= iso_df[iso_df['Date'].dt.year > 2018]
        # print(iso_df)

        # Set isoquants - Starts Here

        fig= plt.figure(figsize=(12,8)) 
        a = np.arange(-0.001,np.max(iso_df.value_D)*1.25,np.max(iso_df.value_D)/500) # set 1st isoquant values
        qx =pd.DataFrame.max(iso_df.value)
        qn =pd.DataFrame.min(iso_df.value)

        b = (.75*(qx-qn))/a #set 1st isoquant values
        c = (.5*(qx-qn))/a #set 2nd isoquant values
        d = (.25*(qx-qn))/a #set 3rd isoquant values
        e = (.10*(qx-qn))/a #set 4th isoquant values
        f = iso_df.DV.mean()
        g = iso_df.value_D.mean()


        p2 = plt.plot(a,b,'--', c='Black') # plot isoquant
        p3 = plt.plot(a,c,'--', c='Black')  # plot isoquant
        p4 = plt.plot(a,d,'--', c='Black')  # plot isoquant
        p5 = plt.plot(a,e,'--', c='Black') # plot isoquannt
        p6 = plt.plot([0.001,np.max(iso_df['value_D'])*1.25], [f, f], '--', lw=1, c= 'b' )
        p7 = plt.plot([g,g],[np.min(iso_df.DV)*.5,np.max(iso_df.DV)*1.1],'--',lw = 1, c= 'b')



        p1 = plt.scatter(iso_df['value_D'],iso_df.DV, s= 100, alpha=0.75,\
                     edgecolor = "black", c="#ffd530", linewidth =2, marker="o")

        plt.ylim(np.min(iso_df.DV)*.5,np.max(iso_df.DV)*1.1)
        plt.xlabel(iso_df.Denominator.unique()[0],fontweight ='1000',c="black",fontstyle = 'italic',fontsize = 10)
        plt.ylabel(iso_df.Driver.unique()[0],fontweight ='1000',c="black",fontstyle = 'normal', fontsize = 10)
        #plt.annotate("HERE",(3,6), xytext=(3.5,6.5),ha='center')
        name =  'Isoquants-'+iso_df.Denominator.unique()[0]+'.png' 
        plt.savefig(name)
 #       plt.show()
        return
    
    def Chart_SOC(fmerged_df,Company):
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        from itertools import cycle, islice

        dvfmerged_df = Filter.Filter_Company(fmerged_df,Company) #Filter by Company
        # dvfmerged_df.info()

        start = dvfmerged_df[dvfmerged_df.Date==dvfmerged_df.Date.min()] # Set min date (will be changed to a user input)
        end = dvfmerged_df[dvfmerged_df.Date==dvfmerged_df.Date.max()] #Set max date (will be changed to a user input)

        soc_df= [start,end] # create new list
        soc_df = pd.concat(soc_df) #convert to dataframe for filtering and creating driver values
        soc_df['DV']=soc_df.loc[:,'value']/soc_df.loc[:,'value_D'] #create driver values
        soc_df = soc_df[['Date','Name','Driver','DV']] #make a copy for the SOC charting

        dfp = soc_df.pivot(index="Date",columns='Driver', values="DV")

        #  Step 4: Load and split arrays
        array = dfp.to_numpy()
        startpoint = array[0]
        endpoint = array[1]
        startvalue = startpoint.prod()

        #step 5: Pass and Return from function
        ans = Source_of_Change(startpoint,endpoint)

        # Step 6: Combine and join to Labels
        plotdf = pd.DataFrame(ans, columns = [("DriverValue")])
        Labels = soc_df["Driver"].unique()
        Labels = pd.DataFrame(Labels, columns =["Driver"])
        new = Labels.join(plotdf)
        newsorted = new

        # Step 7: Sort by Value CAN BE OPTIONAL for non-arching plots
        newsorted = new.sort_values(by = ['DriverValue'], ascending = False)
        newsorted = newsorted.reset_index(drop = True)

        # Step 8: Adds new row for start point and then re-indexes
        newsorted.loc[-1] = ["Start", startvalue]  # adding a row
        newsorted.index = newsorted.index + 1  # shifting index
        newsorted = newsorted.sort_index()  # sorting by index

        # Step 9: Creates Blank Series
        invis = newsorted.DriverValue.cumsum().shift(1).fillna(0)
        newsorted["invisible"]= invis

        # Step 10: Get the net total number for the final element in the waterfall and add to dataframe
        total = newsorted.sum().DriverValue
        items = newsorted.index.size
        newsorted.loc[items]= ["End",total,0]
        # print(np.round(total,3) == np.round(np.prod(endpoint),3))
        # print (np.round(total,3)," vs", np.round(np.prod(endpoint),3))

        # Step 11: Combine into original dataset, filter and plot 
        newsorted['Scenario'] = ("Change Values")  # adding the label for scenario
        newsorted['Date']= pd.datetime.now()  # adding the current date to Date
        newsorted = newsorted[['Date','Scenario','Driver','DriverValue','invisible']] #resorting colunms to combine with original dataset
        datasetnew = newsorted


        # Step 12 Add Color for Bars to dataframe
        datasetnew.loc[datasetnew['DriverValue'] < 0.0, 'BarColor'] = 'Red'
        datasetnew.loc[datasetnew['DriverValue']  > 0.0, 'BarColor'] = 'Green'
        datasetnew.loc[datasetnew['DriverValue'] == 0, 'BarColor'] ="#b4b2b3" 
        datasetnew.loc[datasetnew.Driver == ('Start'), 'BarColor']= "Blue"
        datasetnew.loc[datasetnew.Driver == ('End'), 'BarColor']= "Blue"

        # Step 13 Plot
        from matplotlib.ticker import FormatStrFormatter



        fig = plt.figure(figsize=(12,8))

        plt.axhline(linewidth=1, color='k', zorder = 0)
        plt.bar(datasetnew.Driver, datasetnew.DriverValue, bottom=datasetnew.invisible, \
                     color=datasetnew.BarColor,width=.9, edgecolor = "k")
        plt.title = ("Source of Change")
        plt.xlabel("Drivers", fontsize = 18, color = '#000000')
        plt.ylabel("Change Values", fontsize = 18, color = "#000000")
        plt.tight_layout()
        plt.xticks(rotation=-15, ha = 'left', fontsize = 12)
        plt.yticks()
        plt.box(True)
        plt.margins(0.025)




        plt.savefig("PowerBI waterfall.png")
 #       plt.show()
        return datasetnew

    
    ''' 
    CHART CLASS ENDS HERE
    
    '''

    
def cagr(start_value, end_value, num_periods): #function to produce a CAGR
    return (end_value / start_value) ** (1 / (num_periods - 1)) - 1 
''' This function produces a CAGR.  It can be used with other functions to 
    filter time periods, drivers, Numerators and other attributes
'''

def Calc_DriverValue(fmerged_df,SelDriver):
    ''' This function produces a new column for dynamically calulated Driver Value(DV).  It can be used with other functions to 
    filter time periods, drivers, Numerators and other attributes
    '''
    fmerged_df['DV'] = fmerged_df['value']/fmerged_df['value_D']
    dvmerged_df = fmerged_df
    return dvmerged_df

''' BIG TRANSFORMATION''' #Need to be checked

def Source_of_Change(a,b):
    
    import numpy as np
    import pandas as pd
    np.seterr(divide='ignore', invalid='ignore')

    # Step 1
    A = a
    # Step 2
    B = b
    # Step 3
    C = B-A
    # Step 4
    D = np.sign(A)*C/A
    

    y = np.size(A)

    COLUMN = 2**np.arange(0,y).reshape(1,y) #develop the column values
    ROW = np.arange(2**y).reshape(2**y,1) # develop the row values

    E = np.remainder((ROW//COLUMN),2)  #creating the binary array for toggling changes

    F = (E == 0).astype(float) #creating the binary array for toggling start values (mirror of E)

    # Step 5 
    DIFF = E * C

    # Step 6
    START = F * A

    # Step 7
    COMBINED = DIFF + START

    # Step 8
    DELTAS = np.prod(COMBINED, axis =1).reshape(2**y,1)

    # Step 9
    DENOM = np.nan_to_num(((E*np.absolute(D))@np.ones(y))).reshape(2**y,1)

    # Step 10
    ALLOCATED_DELTAS = (E*np.absolute(D))/(DENOM)*DELTAS
    ALLOCATED_DELTAS = np.nan_to_num(ALLOCATED_DELTAS)

    # Step 11
    ANSWER = np.ones(2**y)@ALLOCATED_DELTAS  
    total = sum(ANSWER)
    
    np.set_printoptions(precision=3,suppress=True)
#     print(COMBINED)  
#     print(ANSWER)
#     print(ALLOCATED_DELTAS)
#     print(DENOM)

    return ANSWER

# Step 2.X: Create the isoquant Chart for a factor and return a chart



def Waterfall (ans, dataset, startvalue):
    import pandas as pd
    import matplotlib.pyplot as plt 
    
    # Step 6: Combine and join to Labels
    plotdf = pd.DataFrame(ans, columns = [("DriverValue")])
    Labels = dataset["Driver"].unique()
    Labels = pd.DataFrame(Labels, columns =["Driver"])
    new = Labels.join(plotdf)
    newsorted = new

    # Step 7: Sort by Value CAN BE OPTIONAL for non-arching plots
    newsorted = new.sort_values(by = ['DriverValue'], ascending = False)
    newsorted = newsorted.reset_index(drop = True)

    # Step 8: Adds new row for start point and then re-indexes
    newsorted.loc[-1] = ["Start", startvalue]  # adding a row
    newsorted.index = newsorted.index + 1  # shifting index
    newsorted = newsorted.sort_index()  # sorting by index

    # Step 9: Creates Blank Series
    invis = newsorted.DriverValue.cumsum().shift(1).fillna(0)
    newsorted["invisible"]= invis

    # Step 10: Get the net total number for the final element in the waterfall and add to dataframe
    total = newsorted.sum().DriverValue
    items = newsorted.index.size
    newsorted.loc[items]= ["End",total,0]

    # Step 11: Combine into original dataset, filter and plot 
    newsorted['Scenario'] = ("Change Values")  # adding the label for scenario
    newsorted['Date']= pd.datetime.now()  # adding the current date to Date
    newsorted = newsorted[['Date','Scenario','Driver','DriverValue','invisible']] #resorting colunms to combine with original dataset
    datasetnew = newsorted


    # Step 12 Add Color for Bars to dataframe
    datasetnew.loc[datasetnew['DriverValue'] < 0.0, 'BarColor'] = 'Red'
    datasetnew.loc[datasetnew['DriverValue']  > 0.0, 'BarColor'] = 'Green'
    datasetnew.loc[datasetnew['DriverValue'] == 0, 'BarColor'] ="#b4b2b3" 
    datasetnew.loc[datasetnew.Driver == ('Start'), 'BarColor']= "Blue"
    datasetnew.loc[datasetnew.Driver == ('End'), 'BarColor']= "Blue"

    # Step 13 Plot

    fig = plt.figure(figsize=(15,5))
    plt.axhline(linewidth=1, color='k', zorder = 0)
    plt.bar(datasetnew.Driver, datasetnew.DriverValue, bottom=datasetnew.invisible, \
             color=datasetnew.BarColor,width=.9, edgecolor = "k")
    plt.title = ("Source of Change")
    #plt.xlabel("Drivers", fontsize = 18, color = '#000000')
    plt.ylabel("Change Values", fontsize = 18, color = "#000000")
    plt.tight_layout()
    plt.xticks(rotation=-15, ha = 'left', fontsize = 12)
    plt.yticks()
    plt.box(True)
    plt.margins(0.025)
    plt.savefig("PowerBI waterfall.png")
    plt.show()
    return

# This module creates the standard sparkline charts






