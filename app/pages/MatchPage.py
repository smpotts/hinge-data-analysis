from dash import html, dcc
import pandas as pd
import dash_mantine_components as dmc
import plotly.express as px

from analytics.MatchAnalytics import MatchAnalytics

def message_counts_boxplot():
    message_counts = MatchAnalytics().get_message_count_last_12_months()

    df = pd.DataFrame(message_counts)
    # change the month to a date so we can sort it and then convert it back to a string
    df["month"] = pd.to_datetime(df["month"])
    df = df.sort_values("month")
    df["month"] = df["month"].dt.strftime("%Y-%m")

    fig = px.box(
        df,
        x="month",
        y="message_count",
        height=600, # increase height
        # title="Message Counts per Match by Month (Last 12 Months)",
        labels={"month": "Month", "message_count": "Number of Messages"},
        points="all"  # show individual data points too
    )
    fig.update_layout(xaxis_tickangle=-45)

    return dmc.Card(
        children=[
            dmc.Space(h=10),
            dmc.Text("Message Count Variability by Month (Last 12 Months)", weight=700, size="xl"),
            dmc.Space(h=10),
            dmc.Text("This box plot shows how the number of messages exchanged per match varies across each month over the past year. Each box represents the distribution of message counts for matches that had at least one message in that month. The plot highlights patterns in user engagement, such as which months tend to have higher or lower activity, and reveals any outliers — matches with unusually high or low message counts. This can be useful for identifying seasonal trends or behavioral shifts in how users interact over time.", size="md"),
            dmc.Space(h=10),
            dcc.Graph(figure=fig)  
        ],
        # withBorder=True,
        shadow="sm",
        radius="md",
        style={"height": "750px"},
    )


layout = html.Div([
        dmc.Text("Match Analytics", align="center", style={"fontSize": 28}, weight=500),
        dmc.Text("This section reveals patterns in the user's matching behavior, preferences, and key factors that influence successful connections with potential matches."),
        dmc.Space(h=20),
        message_counts_boxplot()
    ])
