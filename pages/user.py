from dash import html
import dash_mantine_components as dmc
from dash import dcc, Input, Output, callback
import plotly.express as px
from dash.exceptions import PreventUpdate

import user_analytics as ua


layout = html.Div([
    html.Button('Reload Graphs', id='refresh-page',
                style={"fontSize": 16, 'font-family': "Open Sans, verdana, arial, sans-serif"}),
    dmc.Space(h=20),
    dmc.Text("User Analytics", style={"fontSize": 28}, weight=500),
    dmc.Text("This section contains insights about your user data that was collected while you were using Hinge."),
    dmc.Space(h=20),

    # user latitude and longitude coordinates
    dmc.Text("Where you've used the app", size="xl", align="center", weight=500),
    dmc.Text("This takes the public IP addresses from the sessions where you used Hinge and uses that to look up the "
             "latitude and longitude coordinates to show where you were when you were using the app. This is limited "
             "to 100 sessions."),
    # TODO: figure out what to do with this map because it's god awful to run
    dcc.Graph("live-update-coords-graph"),
])


@callback(
    Output('live-update-coords-graph', 'figure'),
    [Input('refresh-page', 'n_clicks')]
)
def update_coords_graph_live(data):
    if data is None:
        raise PreventUpdate

    # initial setup of the global events
    user_coordinates = ua.parse_user_ip_addresses()
    # create the funnel graph
    figure = px.scatter_geo(user_coordinates, locationmode="USA-states", lat="latitude", lon="longitude",
                projection="orthographic")
    return figure