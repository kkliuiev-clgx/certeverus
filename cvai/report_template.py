import plotly.graph_objects as go
import plotly.io as pio

def selected_report_template(sel='web'):
    selection = sel
    return selection

# plotly_template = pio.templates["plotly"]
# print(plotly_template.layout)

# pdf_reports Template

fig = go.Figure(layout = {
                    'annotations':[{'font':{'size':9,'color':'black',}},{'xanchor':'center'}],
                    'font':{'size':9,'color':'black'},
                    'legend':{'font':{'size':6,'color':'black',}},
                    'xaxis': {'automargin': True,
                        'gridcolor': 'white',
                        'linecolor': 'white',
                        'ticks': 'outside',
                        'tickfont': {'size':8, 'color':'black'},
                        'title': {'standoff': 10},
                        # 'type':'date',
                        'showticklabels':True,
                        'zeroline':True,
                        'zerolinecolor': 'Grey',
                        'zerolinewidth': 1},
                    'yaxis': {'automargin': True,
                        'gridcolor': 'white',
                        'linecolor': 'white',
                        'ticks': 'outside',
                        'tickfont': {'size':8, 'color':'black'},
                        'title': {'standoff': 10},
                        'zeroline':True,
                        'zerolinecolor': 'red',
                        'zerolinewidth': 1}}
                        
)
templated_fig = pio.to_templated(fig)
pio.templates['pdf_reports'] = templated_fig.layout.template

fig = go.Figure(layout = {
                    'annotations':[{'font':{'size':24,'color':'black',}},{'xanchor':'center'}],
                    'font':{'size':24,'color':'black'},
                    'legend':{'font':{'size':18,'color':'blue',}},
                    'xaxis': {'automargin': True,
                        'gridcolor': 'white',
                        'linecolor': 'white',
                        'ticks': 'outside',
                        'tickfont': {'size':14, 'color':'black'},
                        'title': {'standoff': 10},
                        # 'type':'date',
                        'showticklabels':True,
                        'zeroline':True,
                        'zerolinecolor': 'Grey',
                        'zerolinewidth': 1},
                    'yaxis': {'automargin': True,
                        'gridcolor': 'white',
                        'linecolor': 'white',
                        'ticks': 'outside',
                        'tickfont': {'size':14, 'color':'black'},
                        'title': {'standoff': 10},
                        'zeroline':True,
                        'zerolinecolor': 'red',
                        'zerolinewidth': 1}}
                
)
templated_fig = pio.to_templated(fig)
pio.templates['web'] = templated_fig.layout.template

# print(pio.templates['plotly'].layout)

