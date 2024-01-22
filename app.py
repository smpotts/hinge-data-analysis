"""
Hinge Data Analysis
"""
__author__ = "Shelby Potts"
__version__ = "0.0.0"

import plotly.express as px
from dash import Dash, html, dash_table, dcc
import dash_mantine_components as dmc
import utils.data_utility as du
import utils.match_analytics as ma

# Initialize the app - incorporate a Dash Mantine theme
external_stylesheets = [dmc.theme.DEFAULT_COLORS]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# capture the normalized_events
normalized_events = du.load_match_data()
# persist DataFrame with total counts
totals_df = ma.total_counts(normalized_events)
# get the breakdown of single vs double likes given just the normalized events that are 'likes'
like_freq_df = ma.analyze_double_likes(normalized_events[normalized_events["type"] == "like"])
# counts of likes with and without comments
like_w_wo_comments_df = ma.analyze_outgoing_likes(normalized_events)
# capture action types per day
action_type_freq_per_day = ma.activity_by_date(normalized_events)

app.layout = html.Div([
    dmc.Title('Hinge Data Analysis', color="black", size="h1"),
    # funnel graph showing breakdown of interactions
    dmc.Text("Interaction Funnel", size="lg", align="center", weight=500),
    dmc.Text("This funnel represents the funnel of your interactions with people on Hinge. The outermost layer "
             "represents the total number of interactions you had (outgoing likes, incoming likes, and people blocked "
             "from the deck. Then it shows the number of outgoing likes sent, matches received, and conversations "
             "started from those matches.", align="center"),
    dcc.Graph(figure=px.funnel(totals_df, x=totals_df["count"], y=totals_df["action_type"])),

    # side by side pie charts drilling into specifics of outgoing likes
    dmc.Text("Details About Outgoing Likes", size="lg", align="center", weight=500),
    dmc.Text("This is a deep dive into your outgoing likes. The pie chart on the left shows a breakdown of the rare"
             " cases where Hinge shows you a users you have already sent an outgoing like to vs the users you liked"
             " once. The pie chart on the right shows how many outgoing likes you sent where you left a comment on the"
             " other person's profile.", align="center"),
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dcc.Graph(figure=px.pie(like_freq_df, values="Count", names="Like Frequency",
                      title="Number of Outgoing Likes per Person"),
                      style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(figure=px.pie(like_w_wo_comments_df, values="Count", names="Likes With/ Without Comments",
                                    title="Outgoing Likes with Comments"),
                      style={'width': '50%', 'display': 'inline-block'}
                      )
        ]),
    ]),

    # line chart showing activity type frequencies by day
    dmc.Text("Counts of Activity Types per Day", size="lg", align="center", weight=500),
    dmc.Text("This line graph displays the counts of each action type (likes, matches, chats, and blocks aka unmatches)"
             " per day over the period of time you have been on Hinge. The legend on the right lists each of the"
             " different action types, and you can select/ unselect different types to look at particular ones.",
             align="center"),
    dcc.Graph(figure=px.line(action_type_freq_per_day, x=action_type_freq_per_day['activity_date'],
                             y=action_type_freq_per_day['count'],
                             color=action_type_freq_per_day['type']))


    # TODO: get rid of this junk...
    # dash_table.DataTable(data=totals_df.to_dict('records'), page_size=10)
])


if __name__ == '__main__':
    app.run(debug=True)

