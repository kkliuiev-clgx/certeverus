"""
This method will manage how we create the figure for the Prescriptions page
Created on Sun Jan 02 2022 - 11:25:04
@author: michaelprinci
"""
import pandas as pd
# import plotly.graph_objects as go
try:
    import derivatives as dv
    import PlotWaterfall as pwf
    import Waterfall_Transformation as wt
    # import plot_table as pt
    import plotNodeMap as pnm
except ImportError:
    from cvai import derivatives as dv
    from cvai import PlotWaterfall as pwf
    from cvai import Waterfall_Transformation as wt
    # from cvai import plot_table as pt
    from cvai import plotNodeMap as pnm

# import derivatives as dv
from plotly.subplots import make_subplots

# import transformation_manager as tm


def create_local_test():
    """
    This method creates a test dataset and figures for running the main function locally
    Created on Sun Jan 02 2022 - 10:56:41
    @author: michaelprinci

    @Returns
        -------
        wftest1_step4, actions_table, wftest2_step4, nodes as plotly figures

    """
    wftest = pd.read_csv(r'./cvai/data/testsets/df_into_fsoc.csv', index_col=0)
    drivers = 'Net Sales'
    wftest1_step2 = wt.FilterSOCdates(
        wftest, "2020-08-01", "2020-09-30", pva=True)
    wftest1_step3 = wt.get_waterfall(
        wftest1_step2, drivers, is_sorted=False, parent_variable="Net Sales", pva=True)
    wftest1_step4 = pwf.plotWaterfall(
        wftest1_step3, "Net Sales", True, "2020-09-30")

    wftest2_step2 = wt.FilterSOCdates(
        wftest, "2020-08-01", "2020-09-30", pva=False)
    wftest2_step3 = wt.get_waterfall(
        wftest2_step2, drivers, is_sorted=False, parent_variable="Net Sales", pva=False)
    wftest2_step4 = pwf.plotWaterfall(
        wftest2_step3, "Net Sales", False, "2020-09-30")

    nodetest = pd.DataFrame()
    nodetest = wftest[['Scenario', 'Num Value', 'Numerator']].copy()
    nodes = pnm.createMap(nodetest, "Net Sales", "prescriptions")

    actions_table = dv.main()

    # print(f'{a=} \n {b=} \n {fig1.data[0]=}')
    return wftest1_step4, actions_table, wftest2_step4, nodes

# Make Plots here


def create_product_page(waterfall1, waterfall2, actions_table, nodes=None):
    """
    This method will create the chart for the Prescriptions Page
    Created on Sun Jan 02 2022 - 11:21:59
    @author: michaelprinci

    @Parameters
        ----------
    waterfall1: fig
    waterfall2: fig
    actions_table: fig
    nodes=None (optional): fig

    @Returns
        -------
    fig: object
    """
    # print(f'{waterfall1=}, {waterfall2=}, {nodes=}, {actions_table=}')
    # Step 1: Get Subplot charts
    # waterfall1 = None   # For testing
    wf1_title = waterfall1.layout.title.text if waterfall1 is not None else None
    wf_noplan_size = 1 if waterfall1 is not None else 2

    # Step 2: Create Fig for adding data
    fig = make_subplots(rows=3, cols=2, row_heights=[.05, .475, .475], column_widths=[0.4, 0.6],
                        horizontal_spacing=.1, vertical_spacing=.25,
                        specs=[[{"type": "domain", "colspan": 2}, None],
                               [{"type": "waterfall", "rowspan": wf_noplan_size}, {
                                   "type": "table", "rowspan": 2}],
                               [{"type": "waterfall"}, None]],
                        subplot_titles=(
                            None, waterfall2.layout.title.text, "Suggested Actions", wf1_title)
                        )
    # Step 3: Add Nodes
    if nodes is not None:
        for i in range(0, len(nodes.data)):
            fig.add_trace(nodes.data[i], row=1, col=1)
            fig.data[i].domain.x = nodes.data[i].domain.x
            fig.data[i].title.font.size = 8

    # Step 4: Add Table
    fig.add_trace(actions_table.data[0], row=2, col=2)


    # Add Waterfalls: 

    if waterfall1 is not None:
        fig.add_trace(waterfall1.data[0], row=3, col=1)
        fig.update_annotations(yshift= 10, selector=dict(
            text=waterfall1.layout.title.text))
        # annotations = []
        # annotations.extend([waterfall1.layout.annotations, fig.layout.annotations])
        # print(annotations)
        # fig.layout.annotations =annotations 
    fig.add_trace(waterfall2.data[0], row=2, col=1)
    fig.update_traces(cliponaxis=False, selector=dict(type='waterfall'))
    fig.update_traces(title_font_size=12, selector=dict(type='indicator'))
    fig.update_xaxes(automargin=True)
    fig.update_layout(
        showlegend=False,
        annotationdefaults_font_size=12,
        font_size=12,
        title_pad_b=50
    )
    fig.update_traces(overwrite=True, title_font_size=12,
                      selector=dict(type='indicator'))
    fig.update_annotations(yshift= 10, selector=dict(
        text=waterfall2.layout.title.text))

    # print(f'{fig=}')
    # fig.show()
    return fig


# waterfall1, actions_table, waterfall2, nodes = create_local_test()
# create_product_page(waterfall1, waterfall2,actions_table,nodes).show()



""" NEW VERSION """

# def create_product_page(waterfall1, waterfall2, actions_table, nodes=None):
#     """
#     This method will create the chart for the Prescriptions Page
#     Created on Sun Jan 02 2022 - 11:21:59
#     @author: michaelprinci

#     @Parameters
#         ----------
#     waterfall1: fig
#     waterfall2: fig
#     actions_table: fig
#     nodes=None (optional): fig

#     @Returns
#         -------
#     fig: object
#     """

#     data = []
#     layout = []
#     annotations = []

#     if nodes is not None:
#         for i in range(0, len(nodes.data)):
            
#             fig.add_trace(nodes.data[i], row=1, col=1)
#             fig.data[i].domain.x = nodes.data[i].domain.x
#             fig.data[i].title.font.size = 8

#     data.append[waterfall1[0],waterfall2[0]]






#     # Build figure
#     fig = go.Figure(data, layout)

#     fig.update_layout(annotations)

#     print(fig)
#     fig.show()
#     return fig