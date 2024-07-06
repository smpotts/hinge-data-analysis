from dash import html
import dash_mantine_components as dmc
from dash import dcc, Input, Output, callback, dash_table
import plotly.express as px
from dash.exceptions import PreventUpdate

import analytics
import user_analytics as ua


layout = html.Div([
    html.Button('Reload Graphs', id='refresh-page',
                style={"fontSize": 16, 'font-family': "Open Sans, verdana, arial, sans-serif"}),
    dmc.Space(h=20),
    dmc.Text("User Analytics", align="center", style={"fontSize": 28}, weight=500),
    dmc.Text("This section contains insights about your user data that was collected while you were using Hinge."),
    dmc.Space(h=20),

    # table showing account data
    dmc.Text("User Account Info", size="xl", align="left", weight=500),
    dmc.Text("This table shows the account data that was collected while you were using Hinge. This includes data "
             "about when you downloaded the app, the last time you paused or unpaused the app, and the last time "
             "you logged in.", align="left"),
    dmc.Space(h=10),
    html.Div([
        dash_table.DataTable(id='datatable-interactivity'),
        html.Div(id='acct-datatable-interactivity-container'),
    ]),

    dmc.Space(h=20),
    # user latitude and longitude coordinates
    dmc.Text("Where you've used the app", size="xl", align="left", weight=500),
    dmc.Text("This takes the public IP addresses from the sessions where you used Hinge and uses that to look up the "
             "latitude and longitude coordinates to show where you were when you were using the app. This is limited "
             "to 100 sessions.", align="left"),
    # TODO: figure out what to do with this map because it's god awful to run
    dcc.Graph("live-update-coords-graph"),
])


@callback(
    Output('acct-datatable-interactivity-container', 'children'),
    [Input('refresh-page', 'n_clicks')]
)
def update_comment_table(data):
    __check_for_live_update_data(data)

    account_data = analytics.import_user_account_data()
    # passing in the account data as a list for the DataTable
    return [
        dash_table.DataTable(data=[account_data], page_size=5,
                             style_cell={'textAlign': 'left'})
       ]


@callback(
    Output('live-update-coords-graph', 'figure'),
    [Input('refresh-page', 'n_clicks')]
)
def update_coords_graph_live(data):
    __check_for_live_update_data(data)

    # initial setup of the global events
    user_coordinates = ua.parse_user_ip_addresses()
    # create the funnel graph
    figure = px.scatter_geo(user_coordinates, locationmode="USA-states", lat="latitude", lon="longitude",
                projection="orthographic")
    return figure


# TODO: I don't like this this is repeated in both files, consolidate at some point
def __check_for_live_update_data(data):
    if data is None:
        raise PreventUpdate