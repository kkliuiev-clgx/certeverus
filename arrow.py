# import chart_studio.plotly as py
import plotly.graph_objs as go
import numpy as np

trace1 = go.Scatter(
x=[5, 1, 2, 4],
y=[9, 15, 8, 11],
text=['...'],
mode='markers',
name = '2016',
marker=dict(
    size=[125, 50, 110, 75],
    color = 'rgba(152, 0, 0, .8)',
    line = dict(
        width = 2,
        color = 'rgb(0, 0, 0)'
    )
))
trace2 = go.Scatter(
x=[3, 1, 3, 2],
y=[4, 12, 19, 10],
text=['Likelihood: 1</br>Velocity: 1</br>Impact: 1', 'Likelihood: 1</br>Velocity: 1</br>Impact: 1', 
      'Likelihood: 1</br>Velocity: 1</br>Impact: 1', 'Likelihood: 1</br>Velocity: 1</br>Impact: 1'],
mode='markers',
name = '2017',
marker=dict(
    size=[80, 40, 150, 120],
    color = 'rgba(255, 182, 193, .9)',
    line = dict(
        width = 2,
    )
))

layout = go.Layout(showlegend=True, title='Inherent Risk', paper_bgcolor='rgb(243, 243, 243)',
plot_bgcolor='rgb(243, 243, 243)',
xaxis=dict(
    title='Likelihood',
    titlefont=dict(
        family='Courier New, monospace',
        size=18,
        color='#7f7f7f'
    )
),
yaxis=dict(
    title='Velocity',
    titlefont=dict(
        family='Courier New, monospace',
        size=18,
        color='#7f7f7f'
    )
), annotations=[
        dict(
            ax=50,
            ay=9,
            
            axref='x',
            ayref='y',
            x=3,
            y=4,
            xref='x',
            yref='y',
            xshift=-np.cos(np.arctan2(9-4,5-3))*125/2,
            yshift=-np.sin(np.arctan2(9-4,5-3))*125/2,
            standoff = 80/2+125/2,
            showarrow=True,
            arrowhead=3,
            arrowsize=1,
            arrowwidth=1.5,
            arrowcolor='#636363'
        ),
        dict(
            ax=1,
            ay=15,
            axref='x',
            ayref='y',
            x=1,
            y=12,
            xref='x',
            yref='y',
            xshift=-np.cos(np.arctan2(15-12,1-1))*50/2,
            yshift=-np.sin(np.arctan2(15-12,1-1))*50/2,
            standoff = 40/2+50/2,
            showarrow=True,
            arrowhead=3,
            arrowsize=1,
            arrowwidth=1.5,
            arrowcolor='#636363'
        ),
        dict(
            ax=2,
            ay=8,
            axref='x',
            ayref='y',
            x=3,
            y=19,
            xref='x',
            yref='y',
            xshift=-np.cos(np.arctan2(8-19,2-3))*110/2,
            yshift=-np.sin(np.arctan2(8-19,2-3))*110/2,
            standoff = 150/2+110/2,
            showarrow=True,
            arrowhead=3,
            arrowsize=1,
            arrowwidth=1.5,
            arrowcolor='#636363'
        ),
            dict(
        ax=4,
        ay=11,
        axref='x',
        ayref='y',
        x=2,
        y=8,
        xref='x',
        yref='y',
        xshift=-np.cos(np.arctan2(11-10,4-2))*75/2,
        yshift=-np.sin(np.arctan2(11-10,4-2))*75/2,
        standoff = 120/2+75/2,
        showarrow=True,
        arrowhead=3,
        arrowsize=1,
        arrowwidth=1.5,
        arrowcolor='#636363'
        )
        ]
)





    # dict(
    #     ax=4,
    #     ay=11,
    #     axref='x',
    #     ayref='y',
    #     x=2,
    #     y=8,
    #     xref='x',
    #     yref='y',
    #     xshift=-np.cos(np.arctan2(11-10,4-2))*75/2,
    #     yshift=-np.sin(np.arctan2(11-10,4-2))*75/2,
    #     standoff = 120/2+75/2,
    #     showarrow=True,
    #     arrowhead=3,
    #     arrowsize=1,
    #     arrowwidth=1.5,
    #     arrowcolor='#636363'
    #     )


data = [trace1, trace2]
fig = go.Figure(data=data, layout=layout)
fig.show()
# py.iplot(fig, filename='bubblechart-arrow')