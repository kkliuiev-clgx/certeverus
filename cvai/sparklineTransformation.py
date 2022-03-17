"""
This is how we will filter for the Sparklines for the Multifactor Drivers


Created on Sat Jul  4 12:25:10 2020

@author: michaelprinci
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
from datetime import date
from dateutil.relativedelta import relativedelta
from charts import utils

try:
    from cvai import filter_manager as fm
    from cvai import EncapsulationManager as em
    from cvai import report_template
except ImportError:
    from cvai import filter_manager as fm
    from cvai import EncapsulationManager as em
    import report_template

def Sparkline(dataset, drivers, driver_dict=None):
    """ This function passes a dataframe and company name to produce the sparklines
    for each of the drivers in a single axes
    """

    template_type = report_template.selected_report_template()
    pio.templates.default = template_type

    Driverset = tuple(dataset.loc[:,'Driver'].unique())
    # dataset.to_csv(r'./ep/sparkline_from_slt_for_ep.csv')
    plotneed = len(Driverset) #counts the number of drivers to set up the subplot rows
    ScenarioList = (dataset.loc[:,'Scenario'].unique())
    colorset = ['#729BC7','#666666', '#077816','#077816']
    dashset = [None,'dot','dash','dot']
    # print("here is the set: ",Driverset) # check  what is passed
    datemin = dataset[dataset.Scenario == ScenarioList[0]].index.min()
    datemax = dataset[dataset.Scenario == ScenarioList[0]].index.max()

    label_dict = utils.get_label_dict(drivers)
    format_dict = utils.get_format_dict(drivers)


    # Uses the dictionary name in place of name listed in Driverset if applicable
    driverset_names = []
    if driver_dict != None:
        for i in Driverset:
            if driver_dict.get(i) != None: 
                driverset_names.append(driver_dict.get(i)) # Appends dictionary names to driverset_names whenever a driver listed in the given dictonary is found
            else:
                driverset_names.append(i)
    else:
        for i in Driverset:
            driverset_names.append(label_dict.get(i))
    
    fig = make_subplots(rows=plotneed, cols=1,
                shared_xaxes=True,
                # vertical_spacing=0.055,
                subplot_titles=driverset_names) # PLotly Set for subplots (Replacing subplot_titles=Driverset)
    plotnum = 1 #initiates the loop
    metric_formats = []

    for x, i in enumerate(Driverset): # For Loop to iterate through the Drivers tuple

        if i == "/": # Checks to see if the Driver is "/" or Blank
            continue # Iterates past Blank Driver
        metric_formats.append(format_dict.get(i))
        fildata = dataset.loc[dataset.loc[:,'Driver'] == i]
        fildata = fildata.rename(columns={'Driver Value':'value'}) if 'Driver Value' in fildata.columns else fildata
        # loop in here based on scenario
        scenariostep = 0

        leg = bool(x==0)
        for j, s in  enumerate(ScenarioList):  #need to change the target to Driver Value
            if s == 'nan':
                continue
           
            # print(leg)

            fig.add_trace(go.Scatter(
                    x=fildata[fildata['Scenario']== s].index,
                    y=fildata[fildata['Scenario']==s]['value'],
                    name = s,
                    legendgroup = s,
                    line=dict(color= colorset[j], width=3, dash= dashset[j]),
                    showlegend = leg),
                    row=plotnum, col=1
             )

            # print(j, s, scenariostep)
            scenariostep += 1
       # increment scenario

        plotnum = plotnum+ 1 #increments the plot position  
    # print(dataset.Parent.iloc[0])
    # print(datemin)


    # TODO: The formatting for each of the plot axes should be updated dynamically rather than manually (may not be possible with plotly)
    if len(metric_formats) == 10:
        fig.update_layout(
                title_text=dataset['Parent'].iloc[0],
                showlegend = False,
                yaxis=dict(tickformat = metric_formats[0]), # Tickformats are manually assigned to each graph, but this will not support any parent values with more or less than 10 values
                yaxis2=dict(tickformat = metric_formats[1]),
                yaxis3=dict(tickformat = metric_formats[2]),
                yaxis4=dict(tickformat = metric_formats[3]),
                yaxis5=dict(tickformat = metric_formats[4]),
                yaxis6=dict(tickformat = metric_formats[5]),
                yaxis7=dict(tickformat = metric_formats[6]),
                yaxis8=dict(tickformat = metric_formats[7]),
                yaxis9=dict(tickformat = metric_formats[8]),
                yaxis10=dict(tickformat = metric_formats[9]),
        )
    else:
        fig.update_layout(
                title_text=dataset['Parent'].iloc[0],
                showlegend = False
        )
              
    fig.update_xaxes(
        ticks = 'inside',
        # tickvals = dataset.index,
        type='date',
        showticklabels=True,
        tick0 = [datemin+relativedelta(months = -1)],
        range = [datemin+relativedelta(months = -1),datemax +relativedelta(months = +6)],
        # dtick="M1",
        # tickformat="%b\n%y",
        showline=True, linewidth=1, linecolor='black',
        zeroline=True, zerolinewidth=1, zerolinecolor='red'
        )

    f_size = pio.templates[template_type].layout.annotationdefaults.font.size
    for i in fig['layout']['annotations']:
        i['font'] = dict(size=f_size)
        i['x']=(0.0)
        i['xanchor']='left'

    return fig
