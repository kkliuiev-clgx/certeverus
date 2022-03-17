import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import cvai.filter_manager as fm
import cvai.EncapsulationManager as em
import plotly
import cvai.singleFactorTransformation as sf
import plotly.io as pio
import cvai.Waterfall_Transformation as wt


def plotCoverSheet(driverParent, targetDriver,targetNum,targetDenom, postedDrivers, postedNum, postedDenom,dataset):

    ScenarioNo  = postedNum.Scenario.unique()
    postedDrivers = postedDrivers if 'value' in postedDrivers.columns else postedDrivers.rename(columns={'Driver Value':'value'})#Gets Scenarios for Plotting
    # print(ScenarioNo)
    # print(driverParent,targetDriver)
    ColorNo = ['#729BC7','#666666']
    dashset = [None,'dot']
    fig = make_subplots(rows=2, cols=1, subplot_titles=(targetDriver, targetNum),specs=[[{}],
            [{}]])
    
    # Driver Traces
         
    fig.append_trace(go.Bar(
        x=postedDrivers.index,
        y= postedDrivers[postedDrivers['Scenario']== ScenarioNo[0]]['value'],
        marker_color = ColorNo[0], name = ScenarioNo[0]), row=1, col= 1 )


    fig.append_trace(go.Scatter(
        x= postedDrivers[postedDrivers['Scenario']== ScenarioNo[1]].index,
        y= postedDrivers[postedDrivers['Scenario']== ScenarioNo[1]]['value'],
        marker_color = ColorNo[1], name = ScenarioNo[1], 
        line=dict( width=2, dash= dashset[1])), row=1, col=1)

    # # Waterfall  Traces

    fig.append_trace(go.Waterfall(
        # name = Parent, 
        orientation = "v", measure = dataset['Measure'],
        x = dataset['Driver'], text = dataset['DriverValue'].round(1),texttemplate='%{text:.2s}',
        textposition = "outside", y = dataset['DriverValue']), row=2,col=1)

    
    fig.update_layout(title = {
        'text': targetDriver,
        'y':0.9,
        'x':0.1,
        }, font = {'size': 8}, showlegend = False)

    for i in fig['layout']['annotations']:
        i['font'] = dict(size=10, color='grey')
    
    
    # filePDF = targetDriver.replace("/"," per ")+" cover.pdf" # sets the file Name
    # pio.write_image(fig,filePDF)  # Writes the PDF File
    # fig.show()

    return fig

# def plot_Cover():
#     pl = plotCoverSheet(driverParent, targetDriver,targetNum,targetDenom, postedDrivers, postedNum, postedDenom, dataset)
#     chart = plotly.io.to_json(pl) 
#     return chart

# driverParent, targetDriver,targetNum,targetDenom, postedDrivers, postedNum, postedDenom = sf.plot_singleFactor()
# dataset = wt.plot_waterfall()
# dataset.to_csv('dataforWF.csv')

# plot_Cover()

  