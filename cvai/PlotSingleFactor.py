"""
This is how we will Plot Single Factor Drivers


Created on Sat Jul  4 12:25:10 2020

@author: michaelprinci
"""
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
# import datetime as dt
# from cvai import report_template
# from cvai import web_template
from datetime import date
from dateutil.relativedelta import relativedelta
from charts import utils
# import plotly.io as pio

try:
    from cvai import report_template
#     from cvai import filter_manager as fm
#     from cvai import EncapsulationManager as em
#     from cvai import singleFactorTransformation as sf

except ImportError:
    import report_template
#     import filter_manager as fm
#     import EncapsulationManager as em
#     import singleFactorTransformation as sf

# TODO #357 The system wants to use only the posted drivers file/object


def plotSingleFactor(driverparent, targetdriver, targetnum, targetdenom, 
                     posteddrivers, postednum, posteddenom, driverformat, metricformat, source=None):  # TODO Make last two args optional and equal to None

    template_type = report_template.selected_report_template()
    pio.templates.default = template_type
    # """ Plots Single Factor """
    posteddrivers = posteddrivers.rename(columns={
                                         'value': 'Driver Value'}) if 'value' in posteddrivers.columns else posteddrivers
    # TODO trigger if arg is NOT optional
    postednum = postednum.rename(
        columns={'value': 'Num Value'}) if 'value' in postednum.columns else postednum
    # TODO trigger if ars is Not None
    posteddenom = posteddenom.rename(
        columns={'value': 'Denom Value'}) if 'value' in posteddenom.columns else posteddenom

    # postednum.to_csv(r'./ep/numerators_for_sft_for_ep.csv')
    # posteddenom.to_csv(r'./ep/denominators_for_sft_for_ep.csv')
    # posteddrivers.to_csv(r'./ep/drivers_for_sft_for_ep.csv')

    scenario_no = posteddrivers.Scenario.unique()  # Gets Scenarios for Plotting
    datemin = posteddrivers[posteddrivers.Scenario ==
                            scenario_no[0]].index.min()
    datemax = posteddrivers[posteddrivers.Scenario ==
                            scenario_no[0]].index.max()
    scen_len = len(scenario_no) > 1
    color_no = ['#729BC7', '#666666', '#077816', '#077816']
    dashset = [None, 'dot', 'dash', 'dot']
    # print(posteddrivers.index)
    targettitle = targetdriver if (source == 1) else "Driver Value"
    numtitle = targetnum if (source == 1) else "Num Value"
    denomtitle = targetdenom if (source == 1) else "Denom Value"
    print("COLUMN TITLES: ", targettitle, numtitle, denomtitle)

     # Creates list for how plot axes should be formatted based on their metric
    fig = make_subplots(rows=2, cols=2,
                        subplot_titles=(targetdriver, targetnum, targetdenom),
                        specs=[[{"colspan": 2}, None], [{}, {}]])
    # Driver Traces -  #TODO #358 The APP uses a loop to place traces on the chart
    fig.append_trace(go.Bar(
        x=posteddrivers.index,
        y=posteddrivers[posteddrivers['Scenario']
                        == scenario_no[0]][targettitle],
        # text = posteddrivers[posteddrivers['Scenario']== scenario_no[0]]['Driver Value'],
        # texttemplate='%{y:.2f}',
        # textposition = "outside",
        marker_color=color_no[0], name=scenario_no[0], legendgroup=scenario_no[0], showlegend=True), row=1, col=1)
    if scen_len is True:

        for i, scen in enumerate(scenario_no):
            if i == 0:
                continue
            fig.append_trace(go.Scatter(
                x=posteddrivers[posteddrivers['Scenario']
                                == scenario_no[i]].index,
                y=posteddrivers[posteddrivers['Scenario']
                                == scenario_no[i]][targettitle],
                marker_color=color_no[i], name=scenario_no[i],
                line=dict(width=2, dash=dashset[i]), legendgroup=scenario_no[i], showlegend=True), row=1, col=1)

    # Numerator  Traces  --> These will go back to the postedDrivers file Numerator Value
     # >>>>>>>> TODO Make this refer to Posted_drivers

    fig.append_trace(go.Bar(
        x=postednum.index,
        y=postednum[postednum['Scenario'] == scenario_no[0]][numtitle],
        # text = posteddrivers[postednum['Scenario']== scenario_no[0]]['value'],
        # texttemplate='%{y:.0f}',
        # textposition = "outside",

        marker_color=color_no[0], name=scenario_no[0], legendgroup=scenario_no[0], showlegend=False), row=2, col=1)

    if scen_len is True:
        for i, scen in enumerate(scenario_no):
            if i == 0:
                continue
            fig.append_trace(go.Scatter(
                x=postednum[postednum['Scenario'] == scenario_no[i]].index,
                y=postednum[postednum['Scenario'] == scenario_no[i]][numtitle],
                marker_color=color_no[i], name=scenario_no[i],
                line=dict(width=2, dash=dashset[i]), legendgroup=scenario_no[i], showlegend=False), row=2, col=1)

    # Denominator Traces --> These will go back to the postedDrivers file Numerator Value
     # >>>>>>>>> TODO Make this refer to Posted_drivers
    fig.append_trace(go.Bar(
        x=posteddenom.index,
        y=posteddenom[posteddenom['Scenario'] == scenario_no[0]][denomtitle],
        # text = posteddrivers[posteddenom['Scenario']== scenario_no[0]]['value'],
        # texttemplate='%{y:.0f}',
        # textposition = "outside",
        marker_color=color_no[0], name=scenario_no[0], legendgroup=scenario_no[0], showlegend=False), row=2, col=2)
    if scen_len is True:
        for i, scen in enumerate(scenario_no):
            if i == 0:
                continue
            fig.append_trace(go.Scatter(
                x=posteddenom[posteddenom['Scenario'] == scenario_no[i]].index,
                y=posteddenom[posteddenom['Scenario']
                              == scenario_no[i]][denomtitle],
                marker_color=color_no[i], name=scenario_no[i],
                line=dict(width=2, dash=dashset[i]), legendgroup=scenario_no[i], showlegend=False), row=2, col=2)
    # #<<<<<<<<<<<


    fig.update_layout()

    # fig.update_annotations()
    fig.update_xaxes(
        # ticks = 'outside',
        # tickfont = dict(size = 18),
        # tickvals = posteddrivers.index,
        type='date',
        showticklabels=True,

        tick0=[datemin+relativedelta(months=-1)],
        range=[datemin+relativedelta(months=-1),
               datemax + relativedelta(months=+6)],
        # dtick="M3",
        # tickformat="%b\n%y",

        showline=True, linewidth=2, linecolor='black',
        # ticklabelmode="period",
    )

    fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
    # ,zeroline=True, zerolinewidth=1, zerolinecolor='black')
    f_size = pio.templates[template_type].layout.annotationdefaults.font.size
    for i in fig['layout']['annotations']:
        i['font'] = dict(size=f_size)
        # i['x']=(0.0)
        # i['xanchor']='center'
    # filePDF = targetDriver.replace("/"," per ")+" driver.pdf" # sets the file Name
    # pio.write_image(fig,filePDF)  # Writes the PDF File
    # fig.show()
    # print(fig) #test

    fig.update_layout(
       yaxis=dict(tickformat = driverformat),
       yaxis2=dict(tickformat = metricformat[0]),
       yaxis3=dict(tickformat = metricformat[1]),
       showlegend = False

    )

    return fig
