"""
This method will manage the plotting of nodes, their values,
and their comparatives  on the application.
@authors: jordynecottingham, michaelprinci
"""

from datetime import datetime as dt
# import inspect
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def createMap(NumsFile, parent, chart_type="nodemap"):
    """
    This method will create the nodemap for plotting on the Home and Prescriptions Pages
    Created on Sun Jan 02 2022 - 12:31:21
    @author: michaelprinci

    @Parameters
        ----------
    NumsFile: object dataframe
    parent: str
    chart_type="nodemap" (optional): str

    @Returns
        -------
    fig:object
    """

    NumsFile = NumsFile.rename(columns={
        'Num Value': 'value', 'Numerator': 'variable'}) if 'Num Value' in NumsFile.columns else NumsFile
    p = 1
    col_num = NumsFile['variable'].nunique()

    if chart_type == "prescriptions":
        node_rows = 1
        plot1_row = 1
        plot2_row = 1
        speclist2 = [[{"type": "domain"} for x in range(0, col_num)]]
        font_display = 40
    else:
        node_rows = 8
        plot1_row = 2
        plot2_row = 4
        speclist2 = [[{"type": "domain"} for x in range(0, col_num)],
                     [{"type": "domain"} for x in range(0, col_num)],
                     [{"type": "domain"} for x in range(0, col_num)],
                     [{"type": "domain"} for x in range(0, col_num)],
                     [{"type": "domain"} for x in range(0, col_num)],
                     [{"type": "domain"} for x in range(0, col_num)],
                     [{"type": "domain"} for x in range(0, col_num)],
                     [{"type": "domain"} for x in range(0, col_num)]]
        font_display = 40

    fig = make_subplots(
        rows=node_rows, cols=col_num,
        specs=speclist2
    )
    scen_select = "ACTUALS" if "ACTUALS" in NumsFile['Scenario'].unique(
    ) else 'BASELINE'
    # NumsFile.to_csv(r'./ep/nodes_from_PNM_for_EP.csv')

    for n in NumsFile['variable'].unique():
        n_rev = n.replace(' ', '<br />', 1)
        valdf = NumsFile['value'].where(
            (NumsFile['variable'] == n) & (NumsFile['Scenario'] == scen_select))
        # TODO #380 and scenario = Actual - repeat for scenario = plan and use that nmber in place of reference delta placeholder
        valdf = valdf.dropna()
        valdf.index = pd.to_datetime(valdf.index)
        recentval = valdf.iloc[-1]
        priorval = valdf.iloc[-2]
        valdate = valdf.last_valid_index()
        # print(f'At {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno}: {valdate=}')

        if len(NumsFile["Scenario"].unique()) > 1:

            # print(f" At {inspect.getframeinfo(inspect.currentframe()).function} {inspect.getframeinfo(inspect.currentframe()).lineno}:NO PLAN", NumsFile.Scenario.unique())
            plandf = NumsFile['value'].where(
                (NumsFile['variable'] == n) & (NumsFile['Scenario'] == 'PLAN'))
            plandf = plandf.dropna()
            plandf.index = pd.to_datetime(plandf.index)
            plan_num = plandf.loc[valdate]
            comparative = plan_num
            comp_title = 'Planned:'

        else:

            comparative = priorval
            comp_title = 'Prior Month:'

        fig.add_trace(go.Indicator(
            mode="number+delta",
            value=recentval,
            title=n_rev,
            number={"font": {"size": font_display}},
            delta={'reference': comparative, 'relative': True, 'position': "bottom"}),
            row=plot1_row, col=p)

        if chart_type == "nodemap":
            fig.add_trace(go.Indicator(
                mode="number",
                value=comparative,
                title=comp_title,
                number={"font": {"size": 30}}),
                row=plot2_row, col=p)

            # fig.add_trace(go.Indicator(
            #     mode="number+delta",
            #     value=recentval,
            #     title=n_rev,
            #     number={"font": {"size": font_display}},
            #     delta={'reference': priorval, 'relative': True, 'position': "bottom"}),
            #               row=plot1_row, col=p)
            # if chart_type == "nodemap":
            #     fig.add_trace(go.Indicator(
            #         mode="number",
            #         value=priorval,
            #         title="Prior Month:",
            #         number={"font": {"size": 30, "color": 'blue'}}),
            #                   row=plot2_row, col=p)

        p = p + 1

        fig.update_layout(
            # template = 'pdf_reports',
            title={'text': f'<b><i>Nodes for {parent.split("/")[0]} for {dt.strftime(valdate,"%B %Y")}</i></b>\n\n',
                   'font': {"size": 30}
                   }
        )
    # print(fig)
    return fig
