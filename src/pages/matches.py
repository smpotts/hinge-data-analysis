import dash
from dash import html
import dash_mantine_components as dmc

dash.register_page(__name__)

layout = html.Div([
    dmc.Text("Match Analytics", style={"fontSize": 28}, weight=500),
    dmc.Text("This section contains insights about the interactions (likes, matches, chats, and unmatches) you've "
             "had on Hinge."),
    dmc.Space(h=20),
])