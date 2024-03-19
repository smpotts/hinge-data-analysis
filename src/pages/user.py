import dash
from dash import html
import dash_mantine_components as dmc

dash.register_page(__name__)

layout = html.Div([
    dmc.Text("User Analytics", style={"fontSize": 28}, weight=500),
    dmc.Text("This section contains insights about your user data that was collected while you were using Hinge."),
    dmc.Space(h=20),
])