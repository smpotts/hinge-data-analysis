from dash import html
import dash_mantine_components as dmc

# user_coordinates = ua.parse_user_ip_addresses()

layout = html.Div([
    dmc.Text("User Analytics", style={"fontSize": 28}, weight=500),
    dmc.Text("This section contains insights about your user data that was collected while you were using Hinge."),
    dmc.Space(h=20),

    # user latitude and longitude coordinates
    dmc.Text("Where you've used the app", size="xl", align="center", weight=500),
    dmc.Text("This takes the public IP addresses from the sessions where you used Hinge and uses that to look up the "
             "latitude and longitude coordinates to show where you were when you were using the app. This is limited "
             "to 100 sessions."),
    # TODO: figure out what to do with this map because it's god awful to run
    # dcc.Graph(figure=px.scatter_geo(user_coordinates, locationmode="USA-states", lat="latitude", lon="longitude",
    #             projection="orthographic"))
])