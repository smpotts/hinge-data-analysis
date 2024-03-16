import dash
from dash import html
import dash_mantine_components as dmc

dash.register_page(__name__)

layout = html.Div([
    dmc.Space(h=20),
    dmc.Text("Match Analytics", style={"fontSize": 28}, weight=500),
])