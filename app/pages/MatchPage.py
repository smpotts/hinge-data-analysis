from dash import html
import dash_mantine_components as dmc


layout = html.Div([
        dmc.Text("Match Analytics", align="center", style={"fontSize": 28}, weight=500),
        dmc.Text("This section reveals patterns in the user's matching behavior, preferences, and key factors that influence successful connections with potential matches."),
        dmc.Space(h=20),
    ])
