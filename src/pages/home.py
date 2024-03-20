import dash
from dash import html
import dash_mantine_components as dmc

# dash.register_page(__name__, path='/')

layout = html.Div([
    # leave some blank space at the bottom of the page so it's not so crammed
    dmc.Space(h=50),
])