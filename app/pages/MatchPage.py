from dash import html, dcc
import pandas as pd
import dash_mantine_components as dmc
import plotly.express as px

from analytics.MatchAnalytics import MatchAnalytics

match_analytics = MatchAnalytics()

def message_counts_boxplot():
    message_counts = match_analytics.get_message_count_last_12_months()

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
        shadow="sm",
        radius="md",
        style={"height": "750px"},
    )

def response_latency_hist():
    latency_data = match_analytics.get_response_latency()
    fig = px.histogram(
        latency_data,
        x="latency_days",
        nbins=20,
        labels={"latency_days": "Latency (days)"}
    )
    return dmc.Card(
        children=[
            dmc.Space(h=10),
            dmc.Text("Response Latency between Match and First Message Sent", weight=700, size="xl"),
            dmc.Space(h=10),
            dmc.Text("This graph visualizes the response latency, or the time delay between when a match occurs and when the first message is sent." \
            "Shorter latencies may indicate higher levels of engagement or interest, while longer delays could suggest hesitation, lower enthusiasm, or forgotten matches.", size="md"),
            dmc.Space(h=10),
            dcc.Graph(figure=fig)  
        ],
        shadow="sm",
        radius="md",
        style={"height": "520px"},
    )

def match_duration_hist():
    durations = match_analytics.get_match_durations()

    fig = px.histogram(
        durations,
        x="duration_days",
        labels={"duration_days": "Duration (days)"}
    )
    return dmc.Card(
        children=[
            dmc.Space(h=10),
            dmc.Text("Duration of Time Between Match and Remove", weight=700, size="xl"),
            dmc.Space(h=10),
            dmc.Text("This histogram visualizes the duration of a connection and when it was removed or blocked." \
            "Short durations might reflect mismatched expectations, ghosting, or immediate disinterest, while longer " \
            "durations may point to sustained conversations or lingering connections that eventually tapered off. ", size="md"),
            dmc.Space(h=10),
            dcc.Graph(figure=fig)  
        ],
        shadow="sm",
        radius="md",
        style={"height": "520px"},
    )

def match_removal_count_scatter():
    match_rm_counts = pd.DataFrame(match_analytics.get_match_removal_v_count_scatter_data())

    fig = px.scatter(
        match_rm_counts,
        x="message_count",
        y="duration_days",
        labels={
            "message_count": "Messages Exchanged",
            "duration_days": "Days Between Match and Removal"
        },
        opacity=0.7
    )
    fig.update_traces(marker=dict(size=10))

    return dmc.Card(
        children=[
            dmc.Space(h=10),
            dmc.Text("Match Duration vs. Message Count", weight=700, size="xl"),
            dmc.Space(h=10),
            dmc.Text("This scatter plot explores the relationship between the number of messages exchanged in a match and the time until the match was removed or blocked. " \
            "Clusters near the bottom-left corner indicate 'early exits' — matches that were short-lived and involved little to no conversation, often pointing to ghosting or " \
            "instant disengagement. Conversely, matches in the top-right show more sustained interactions before ending.", size="md"),
            dmc.Space(h=10),
            dcc.Graph(figure=fig)  
        ],
        shadow="sm",
        radius="md",
        style={"height": "600px"},
    )


layout = html.Div([
        dmc.Text("Match Analytics", align="center", style={"fontSize": 28}, weight=500),
        dmc.Text("This section reveals patterns in the user's matching behavior, preferences, and key factors that influence successful connections with potential matches."),
        dmc.Space(h=20),
        message_counts_boxplot(),
        dmc.Space(h=20),
        response_latency_hist(),
        dmc.Space(h=20),
        match_duration_hist(),
        dmc.Space(h=20),
        match_removal_count_scatter()
    ])
