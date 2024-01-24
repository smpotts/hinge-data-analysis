"""
Hinge Data Analysis
"""
__author__ = "Shelby Potts"
__version__ = "0.0.0"

import plotly.express as px
from dash import Dash, html, dash_table, dcc
import dash_mantine_components as dmc
import utils.match_analytics as ma
import utils.user_analytics as ua

# Initialize the app - incorporate a Dash Mantine theme
external_stylesheets = [dmc.theme.DEFAULT_COLORS]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# persist DataFrame with total counts
totals_df = ma.total_counts()
# get the breakdown of single vs double likes given just the normalized events that are 'likes'
like_freq_df = ma.analyze_double_likes()
# counts of likes with and without comments
like_w_wo_comments_df = ma.like_comment_ratios()
# capture action types per day
action_type_freq_per_day = ma.activity_by_date()
# get ratio of phone number shares
number_shares = ma.phone_number_shares()
# save commented outgoing likes
commented_likes = ma.commented_outgoing_likes()
# counts of message per chat
chat_counts = ma.date_count_distribution()

header = [
    html.Thead(
        html.Tr(
            [
                html.Th("Like"),
                html.Th("Match"),
                html.Th("Chats"),
                html.Th("Block"),
                html.Th("Meaning"),
            ]
        )
    )
]

row1 = html.Tr([html.Td("X"), html.Td(""), html.Td(""), html.Td(""), html.Td("You sent an outgoing, the person did not like you back")])
row2 = html.Tr([html.Td("X"), html.Td("X"), html.Td("X"), html.Td(""), html.Td("You sent an outgoing like, the other person liked you back, at least one message was exchanged")])
row3 = html.Tr([html.Td(""), html.Td("X"), html.Td("X"), html.Td(""), html.Td("You received an incoming like, you liked the other person back and at least one message was exchanged")])
row4 = html.Tr([html.Td(""), html.Td(""), html.Td(""), html.Td("X"), html.Td("The match was removed or unmatched, can't tell who unmatched who. For some reason, a lot of these exist without any other information and there is no way to tell which interaction it was originally linked to")])
row5 = html.Tr([html.Td(""), html.Td("X"), html.Td(""), html.Td("X"), html.Td("You received an incoming like, you liked the other person back, no messages were exchanged, and the match was removed")])

body = [html.Tbody([row1, row2, row3, row4, row5])]


app.layout = html.Div([
    dmc.Title('Hinge Data Analysis', color="black", size="h1"),
    dmc.Space(h=20),
    dmc.Text("Overview", style={"fontSize": 28}, weight=500),
    dmc.Text("This application is meant to help provide meaningful insights about interactions users have had with "
             "people on the Hinge dating app. Hinge allows users to request an export of their personal data that was "
             "collected while they were using the app. If you have a Hinge account, you can request your data by going "
             "to Settings -> Download My Data. It typically takes between 24 and 48 hours to fulfill this request, and "
             "once the data are ready, Hinge emails you a .zip file with your personal data."),
    dmc.Space(h=20),
    dmc.Text("The data export provided by Hinge contains several files, but the main thing is the index.html file, "
             "which is used to render a webpage with tabs showing different data. The tabs provided by Hinge are "
             "labeled: User, Matches, Prompts, Media, Subscriptions, Fresh Starts, and Selfie Verification. Aside from "
             "viewing changes to your prompts or seeing which pictures you've uploaded, these data are not "
             "particularly useful, especially the Matches tab which is the most disappointing. The Matches tab "
             "contains a list of `matches`, but I actually refer to them as `interactions` in this project because "
             "not all of them are true matches. Needless to say the export provided by Hinge leaves a lot to be "
             "desired, which is why I decided to build this project to analyze and visualize interesting insights "
             "from the Hinge data export."),
    dmc.Space(h=20),
    dmc.Text("Caveats", style={"fontSize": 28}, weight=500),
    dmc.Text("1. Hinge does not provide any documentation about the data in the export so this analysis is based off my"
             "own inferences from working with the data."),
    dmc.Text("2. Hinge occasionally updates and modifies the data they send in the export which may or may not make "
             "aspects of the analysis obsolete or worse, break the program."),
    dmc.Space(h=20),
    dmc.Text("Assumptions", style={"fontSize": 28}, weight=500),
    dmc.Text("Since there is no documentation provided by Hinge, here are some assumptions I am making about the source data: "),
    dmc.Text("1. Unmatches, or `blocks` as Hinge refers to them in the data, could go either direction, meaning you "
             "could have unmatched the other person or they could have unmatched you. Hinge does not include any "
             "additional data in these events to tell who unmatched who."),
    dmc.Text("2. Matches without a like in the same event mean that someone liked you first, and you matched with them"
             " (i.e. there was no outgoing like)"),
    dmc.Space(h=20),
    dmc.Text("Scenario Matrix", style={"fontSize": 28}, weight=500),
    dmc.Text("There are several possible scenarios happening in the export data in what Hinge refers to as `matches`. "
             "These are not all `matches`, because some events are simply outgoing likes that were not reciprocated. "
             "This is why I refer to them as interactions, where an interaction represents the encounters (likes, "
             "matches, chats, blocks) that occurred between you and another person. "),
    dmc.Space(h=10),
    dmc.Text("Here are the different scenarios of interactions that occur in the data: "),
    dmc.Space(h=10),
    dmc.Table(header + body),

    dmc.Space(h=20),
    # funnel graph showing breakdown of interactions
    dmc.Text("Interaction Funnel", size="xl", align="center", weight=500),
    dmc.Text("This funnel represents the funnel of your interactions with people on Hinge. The outermost layer "
             "represents the total number of interactions you had (outgoing likes, incoming likes, and people blocked "
             "from the deck. Then it shows the number of outgoing likes sent, matches received, and conversations "
             "started from those matches.", align="center"),
    dcc.Graph(figure=px.funnel(totals_df, x=totals_df["count"], y=totals_df["action_type"])),

    # side by side pie charts drilling into specifics of outgoing likes
    dmc.Text("Outgoing Likes You've Sent", size="xl", align="center", weight=500),
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

    dmc.Text("What You're Commenting When You Like Someone's Content", size="md", align="left"),
    dash_table.DataTable(data=commented_likes.to_dict('records'), page_size=10, style_cell={'textAlign': 'left'}),

    # line chart showing activity type frequencies by day
    dmc.Text("Frequency of Action Types by Day", size="xl", align="center", weight=500),
    dmc.Text("This line graph displays the counts of each action type (likes, matches, chats, and blocks aka unmatches)"
             " per day over the duration of time you have been on Hinge. The legend on the right lists each of the"
             " different action types, and you can select/ unselect different types to look at particular ones.",
             align="center"),
    dcc.Graph(figure=px.line(action_type_freq_per_day, x=action_type_freq_per_day['activity_date'],
                             y=action_type_freq_per_day['count'],
                             color=action_type_freq_per_day['type'])),

    # pie chart showing percentage of interactions with a phone number share
    dmc.Text("How Many People Did You Give Your Number To?", size="xl", align="center", weight=500),
    dmc.Text("This is the ratio of people you shared your phone number with out of the total number of people you "
             "had chats with. This operates on the assumption you gave your phone number in a standard format, "
             "ex: XXX-XXX-XXXX, XXXXXXXXXX, or (XXX)XXX-XXXX.",
             align="center"),
    dcc.Graph(figure=px.pie(number_shares, values="Count", names="Message Outcomes")),

    # histogram showing the number of outgoing messages in each chat
    dmc.Text("Outgoing Messages Sent per Chat", size="xl", align="center", weight=500),
    dmc.Text("This histogram shows the number of outgoing messages you sent in each chat.",
             align="center"),
    dcc.Graph(figure=px.histogram(chat_counts, x='outgoing_messages', nbins=50).update_layout(bargap=0.2))


    # dcc.Graph(figure=px.scatter_geo(user_coords, locationmode="USA-states", lat="latitude", lon="longitude",
    #             hover_data=["airport", "city", "state", "cnt"],
                # color="cnt",
                # color_continuous_scale=px.colors.cyclical.IceFire,
                # projection="orthographic"))
])




if __name__ == '__main__':
    app.run(debug=True)
