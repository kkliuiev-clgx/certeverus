"""
This method will prepare the table for prescriptions to plot on application page
Created on Mon Jan 03 2022 - 12:57:01
@author: michaelprinci

"""

import plotly.graph_objects as go
# import pandas as pd
# import numpy as np
# import plotly


def plot_table(df):
    """
    This method will plot the table and return a json object for plotly on application
    Created on Mon Jan 03 2022 - 12:57:39
    @author: michaelprinci

    @Parameters
        ----------
    df: object DataFrame

    @Returns
        -------
    fig: Figure
    """
    df = df.reset_index()
    df = df[['index', 'Prescription', 'Additional value', ]].rename(
        {'index': 'Team', 'Additional value': 'Target', 'Prescription': 'Task'}, axis=1)
    df.Target = df['Target'].apply(lambda x: f'${x:,.0f}').astype(str)
    # df['Target'] =  df['Target'].astype(str)

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='#ffffff',
                    align='center'),
        cells=dict(values=df.T*1,
                   fill_color='#ffffff',
                   align='center',
                   font=dict(color='darkslategray', size=20),
                   height=30))])
    # fig.show()
    # print(fig)
    return fig
