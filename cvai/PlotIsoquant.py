
"""
This is how we will for the Isoquant Chart


Created on Sat Jul  4 12:25:10 2020

@author: michaelprinci
"""

import numpy as np
import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio

try:
    from cvai import report_template
except ImportError:
    import report_template


def plotisoquant(driverParent, targetDriver, targetNum, targetDenom,
                 postedDrivers, postedNum, postedDenom, attribs,
                 ytd, driverformat, metricformat, startdate='2020-01-01'):
    """ Plots Isoquant Chart     """
    template_type = report_template.selected_report_template()
    pio.templates.default = template_type

    isodriver, isodenom = postedDrivers, postedDenom
    isodenom = isodenom.rename(columns={
                               'Denom Value': 'value', 'Denominator': 'variable'}) if 'Denom Value' in isodenom.columns else isodenom
    isodriver = isodriver.rename(columns={
                                 'Driver Value': 'value'}) if 'Driver Value' in isodriver.columns else isodriver
    # print("\n\n\n\n\n\n\n",isodenom.value)
    # grouping_element = None if attribs is None else isodriver[attribs].unique()
    # print ("PLOT ISO FN (line 35):\n",isodriver, isodenom, grouping_element, "\n\n",isodriver['Num Value'])
    if isodenom.empty == True:
        # print("%%%%%%%%%%   NONE VALUE FOR A\n")
        a = np.arange(.001, 2, .01)
        horizontal = 'Denominator'

    else:
        # print("$$$$$$$$$$$  CALC VALUE FOR A\n")
        a = np.arange(0.001, isodenom.value.max()*2, isodenom.value.max()/100)
        horizontal = isodenom.variable[0]

    if ytd:
        ytd_label = f' (YTD) from {startdate}'
    else:
        ytd_label = ''

    if attribs is None:
        title_text = f'{targetDriver} vs {isodenom.variable[0]}  {ytd_label}'
    else:
        title_text = f'{targetDriver} vs {isodenom.variable[0]} by {attribs}{ytd_label}'

    # isodenom.to_csv(r'./ep/denominator_for_isoquant_for_ep.csv')
    # isodriver.to_csv(r'./ep/driver_for_isoquant_for_ep.csv')
    '''
    the isoquant value for the plan for a ggiven month will be set to b.  May need to add a conditional to handle non- plan values
    set C to next nmonth plan if plan.
    '''
    b = (isodenom.value.mean()*isodriver.value.mean())/a
    c = (isodenom.value.mean()*isodriver.value.mean()*.50)/a
    d = (isodenom.value.mean()*isodriver.value.mean()*1.25)/a
    ymax = isodriver.value.max()*1.2
    xmin = 0 if isodenom.value.min() > 0 else isodenom.value.min()*1.2
    xmax = isodenom.value.max()*1.2
    ymin = isodriver.value.min()*.8 if isodriver.value.min() > 0 else isodriver.value.min()*1.2
    # print("@@@@@@@@ IOSDRIVER:\n",isodriver)
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=a,
            y=b,
            mode="lines",
            line=go.scatter.Line(color="#ffd530"),
            name=f" {(a*b)[0]:,.0f}",
            showlegend=True)
    )

    fig.add_trace(
        go.Scatter(
            x=a,
            y=c,
            mode="lines",
            line=go.scatter.Line(color="#000000"),
            name=f" {(a*c)[0]:,.0f}",
            showlegend=True)
    )

    fig.add_trace(
        go.Scatter(
            x=a,
            y=d,
            mode="lines",
            line=go.scatter.Line(color="#b2b4b3"),
            name=f" {(a*d)[0]:,.0f}",
            showlegend=True)
    )

    # Sets color by Scenario  -->  THIS WILL REPLACE ISODENOM AND POSTED DENOM for X in Trace
    for i in isodriver['Scenario'].unique():
        if isodenom.empty == True:
            Note = '<br>This chart is intentionally blank.</br><br>The denominator of this driver is 1 and therefore the chart is not presented</br>'

        else:
            Note = ""

        if attribs is None:
            jlist = ['Scenario']

        elif attribs in isodriver.columns:
            jlist = isodriver[attribs].unique()
            print(jlist, isodriver.columns)

        elif attribs + "_resamp" in isodriver.columns:
            attribs = attribs+'_resamp'
            # print(f'rev={attribs}')
            jlist = isodriver[attribs].unique()
            # print(f'jlist:{jlist}, \t {isodriver.columns}')

        else:
            jlist = ['Scenario']

        xx = isodenom[isodenom['Scenario'] == i]
        yy = isodriver[isodriver['Scenario'] == i]
        zz = xx.value*yy.value

        for j in jlist:
            if len(jlist) > 1:
                # TODO #242 add an Attribute Column in postedDenom
                xattrib = isodenom[(isodenom[attribs] == j) & (
                    isodenom['Scenario'] == i)].value
                yattrib = isodriver[(isodriver[attribs] == j) & (
                    isodriver['Scenario'] == i)].value
                name_label = j + " - " + i
            else:
                xattrib = isodenom[(isodenom['Scenario'] == i)].value
                yattrib = isodriver[(isodriver['Scenario'] == i)].value
                name_label = i
            # print(j)
            fig.add_trace(
                go.Scatter(
                    x=xattrib,
                    y=yattrib,
                    text=name_label+" "+isodriver.index.strftime('%b %Y'),
                    name=name_label,
                    # isodenom[isodenom['Scenario']==i].value*isodriver[isodriver['Scenario']==i].value),
                    customdata=(xattrib*yattrib),
                    # hovertemplate = 'who: %{customdata}<br> date: %{text}',
                    hovertemplate="<b>%{text}</b><br>" +
                    "%{yaxis.title.text}: %{y:,.2f}<br>" +
                    "%{xaxis.title.text}: %{x:,.2f}<br>" +
                    "<em>Total = %{customdata:,.1f}</em><br>" +
                    "<extra></extra>",
                    showlegend=True,
                    mode='markers+lines',
                    marker_line_width=.5, marker_size=10, opacity=.7,
                    # marker_color= isodenom['Provider'].unique(),
                    line_width=.25,
                    # transforms = [
                    #     dict(
                    #         type = 'groupby',
                    #         groups = isodriver['CAE']
                    #     )]


                ))

    fig.layout = go.Layout(
        # template = 'pdf_reports',
        # targetDriver replaces title_text
        title=go.layout.Title(text=title_text),
        xaxis=dict(title=horizontal, range=[xmin, xmax]),
        # targetDriver replaces isodriver.Driver[0]
        yaxis=dict(title=targetDriver, range=[ymin, ymax]),

        annotations=[
            go.layout.Annotation(
                text=Note,
                # font = {size:24},
                showarrow=False,
                x=1
            )
        ]
    )
    # Updates the axis formatting
    fig.update_layout(yaxis_tickformat=driverformat,
                      xaxis_tickformat=metricformat[1])
    return fig
