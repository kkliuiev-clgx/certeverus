"""
This is how we will plot the Source of Change for the Multifactor Drivers


Created on Sat Jul  4 12:25:10 2020

@author: michaelprinci
"""
from datetime import datetime as dt

import plotly.graph_objects as go
import plotly.io as pio

from charts import utils

try:
    # from cvai import Waterfall_Transformation as wt
    from cvai import report_template
except ImportError:
    # import Waterfall_Transformation as wt
    import report_template


def plotWaterfall(dataset, parent_var, pva, end_period,  drivers, driver_dict=None, target_scenario='ACTUALS',):
    """
    This method will manage Plotting of Waterfall Chart
    Created on Sun Jan 02 2022 - 12:51:03
    @author: michaelprinci

    @Parameters
        ----------
    dataset: object
    parent_var: str
    pva:boolean
    end_period:str target_scenario='ACTUALS'

    @Returns
        -------
    SocChart: figure
    """
    # print('$$$$$$$$$FROM PW:\n',dataset,'\n *** ',parent_var,'\n INTO PLOTLY WATERFALL $$$$$$$$$$$\n')
    # dataset.to_csv(r'./ep/waterfall_from_pwf_for_ep.csv')

    # dataset = dataset.reset_index();
    target_scenario = 'ACTUALS' if 'ACTUALS' in dataset.Scenario.unique(
    ) else 'BASELINE'  # TODO Check this
    # print(f'Target Scenario: {target_scenario}')
    template_type = report_template.selected_report_template()
    pio.templates.default = template_type

    if not pva:
        pva_label = f'({dataset.Driver.iloc[0]} vs. {dataset.Driver.iloc[-1]})'
        comparison = 'last month'
    else:
        pva_label = f'(Planned vs. {target_scenario.title()} for {dt.strptime(end_period,"%Y-%m-%d"):%b %Y})'
        comparison = f'{dataset.Driver.iloc[0]}'
        # print(dataset)

    xspot = dataset['Driver'].to_list()
    yspot = dataset['DriverValue'].to_list()
    # invisi = dataset['invisible'].to_list()
    y_maxx = yspot[yspot.index(min(yspot))]
    y_place = sum(yspot[0:yspot.index(min(yspot))]) + y_maxx
    y_arrow = sum(yspot[0:yspot.index(min(yspot))])
    # textrem = [x if textspot.index(x) == yspot.index(max(yspot)) else None for x in textspot]
    callout_x = xspot[yspot.index(min(yspot))]

    # text_for_value = textspot[yspot.index(max(yspot))]
    ttext = f'Opportunity of <br /><b>${abs(y_maxx):,.0f}</b><br /> for {callout_x} <br />compared to {comparison}'

    SocChart = go.Figure(go.Waterfall(
        orientation="v",
        measure=dataset['Measure'].to_list(),
        x=dataset['Driver'].to_list(),
        text=dataset['DriverValue'].to_list(),
        texttemplate='%{text:.3s}',
        textposition="outside",
        y=dataset['DriverValue'].to_list(),
        connector={"line": {"color": "#000000"}},
        totals={"marker": {"color": "#729BC7"}}
    ))

    metric_format_dict = utils.get_metric_dict(drivers)

    SocChart.update_layout(
        # template = 'pdf_reports',
        title=("Source of Change - " + \
               parent_var.split("/")[0] + " "+pva_label),
        showlegend=False,
        uniformtext_minsize=8,
        uniformtext_mode='show',
        yaxis=dict(zeroline=True, zerolinewidth=3,
                   zerolinecolor='black',  ticks='outside'),
        yaxis_tickformat=metric_format_dict.get(parent_var.split("/")[0])
        # xaxis = dict(ticks='outside', tickfont=dict(size=10))
    )

    SocChart.add_annotation(
        x=callout_x, y=y_place,
        text=ttext,
        font_color='white',
        font_size=28,
        bgcolor='#b78b20',
        bordercolor='black',
        yshift=-10,
        ax=callout_x,
        ay=y_arrow*.2,
        axref='x',
        ayref='y',
        showarrow=True,
        # arrowhead=1,
        arrowhead=2,
        arrowsize=2,
        arrowwidth=2,
        arrowcolor="#b78b20",
    )
    # filePDF =  dataset.Parent[0].replace("/"," per ")+" Waterfall.pdf" # sets the file Name
    # pio.write_image(SocChart,filePDF);print('Chart Saved')  # Writes the PDF File
    # a = pio.write_image(SocChart,filePDF);print('Chart Saved')  # Writes the PDF File
    # SocChart.show()
    print(SocChart)
    return SocChart
