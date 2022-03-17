import plotly.graph_objects as go
# TODO This is how we can add formatting to the axes for the charts.  Another thing we can add to the configuration file - will need formating for drivers and for the metrics (ie numerator and denominators)


dict_label = {"a":"$"".2f", "b":"%", 'Net Revenue/Visit':'.2%','Visits':'', 'e':'$''.1f'} # This is what we have to replace with a dynamically built ditionary
targ = "Net Revenue/Visit" # this should be passed into to method already
targ2 = "Visits" #this should be in the method already

""" This creates a sampole chart to test format changes"""
fig = go.Figure(go.Scatter(
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    y = [28.8, 28.5, 37, 56.8, 69.7, 79.7, 78.5, 77.8, 74.1, 62.6, 45.3, 39.9]
))

'''
using the dictionary to get the formatting - we will need to add the formats to the configuration file

'''
fig.update_layout(yaxis_tickformat = dict_label.get(targ),
                    xaxis_tickformat = dict_label.get(targ2) )

# fig.show()
