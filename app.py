"""
Hinge Data Analysis
"""
__author__ = "Shelby Potts"
__version__ = "0.0.0"

import pandas as pd
import plotly.express as px
from dash import Dash, html, dash_table, dcc
import dash_mantine_components as dmc
import utils.match_data_utility as mdu
import utils.match_analytics as ma

# Initialize the app - incorporate a Dash Mantine theme
external_stylesheets = [dmc.theme.DEFAULT_COLORS]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# capture the normalized_events
normalized_events = mdu.MatchDataUtility.load_match_data()
# persist DataFrame with total counts
totals_df = ma.MatchAnalytics.total_counts(normalized_events)
# get the breakdown of single vs double likes given just the normalized events that are 'likes'
like_freq_df = ma.MatchAnalytics.analyze_double_likes(normalized_events[normalized_events["type"] == "like"])
# counts of likes with and without comments
like_w_wo_comments_df = ma.MatchAnalytics.analyze_outgoing_likes(normalized_events)

app.layout = html.Div([
    dmc.Title('Hinge Data Analysis', color="black", size="h3"),
    # funnel graph showing breakdown of interactions
    dmc.Text("Interaction Funnel", size="lg", align="center", weight=500),
    dmc.Text("This funnel represents the funnel of your interactions with people on Hinge. The outermost layer "
             "represents the total number of interactions you had (outgoing likes, incoming likes, and people blocked "
             "from the deck. Then it shows the number of outgoing likes sent, matches received, and conversations "
             "started from those matches.", align="center"),
    dcc.Graph(figure=px.funnel(totals_df, x=totals_df["Count"], y=totals_df["Action Type"])),
    # pie chart showing single vs multiple likes
    dmc.Text("Liked Once vs Liked Multiple Times", size="lg", align="center", weight=500),
    dmc.Text("Hinge sometimes shows you people you have already liked before. This is a breakdown of how many people "
             "you sent a single like to and how many people you liked more than once.", align="center"),
    dcc.Graph(figure=px.pie(like_freq_df, values="Count", names="Like Frequency")),
    # pie chart showing outgoing likes that included a comment
    dmc.Text("Outgoing Likes With/ Without Comments", size="lg", align="center", weight=500),
    dmc.Text("This pie chart represents the counts of outgoing likes you sent with and without a comment on the other"
             " person's profile.", align="center"),
    dcc.Graph(figure=px.pie(like_w_wo_comments_df, values="Count", names="Likes With/ Without Comments")),

    # TODO: get rid of this junk...
    dash_table.DataTable(data=totals_df.to_dict('records'), page_size=10)
])


if __name__ == '__main__':
    app.run(debug=True)

