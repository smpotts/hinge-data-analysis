from dash import html
import dash_mantine_components as dmc
from dash import dcc, dash_table, Input, Output, callback
import plotly.express as px
import visdcc

import src.match_analytics as ma

# TODO: open question, how do we cause a reload of the data when the user uploads a new file?
normalized_events = ma.load_match_data("../data/mocked_data/matches.json")
initial_load = True


def reload_global_norm_events(path="../data/app_uploaded_files/matches.json"):

    global initial_load
    initial_load = False
    print(f"inside the reload global norm, initial load: {initial_load}")

    global normalized_events
    # set normalized events with data from the uploads file
    young_fresh_events = ma.load_match_data(path)
    # set the normalized events to the freshly reloaded events
    normalized_events = young_fresh_events


def get_global_norm_events():
    global normalized_events
    return normalized_events


def serve_layout():
    print(f"inside layout, initial load: {initial_load}")
    if not initial_load:
        print(f"inside if not initial load: {initial_load}")
        reload_global_norm_events()

    return html.Div([
        visdcc.Run_js('javascript'),
        html.Button('Refresh Page', id='refresh-page'),


        dmc.Text("Match Analytics", style={"fontSize": 28}, weight=500),
        dmc.Text("This section contains insights about the interactions (likes, matches, chats, and unmatches) you've "
                 "had on Hinge."),
        dmc.Space(h=20),

        # funnel graph showing breakdown of interactions
        dmc.Text("Interaction Funnel", size="xl", align="center", weight=500),
        dmc.Text("This funnel represents the funnel of your interactions with people on Hinge. The outermost layer "
                 "represents the total number of people you interacted with. Then it shows the number of outgoing likes "
                 "you sent, matches received, and conversations started from those matches.", align="center"),
        dcc.Graph(figure=px.funnel(ma.total_counts(normalized_events), x=ma.total_counts(normalized_events)["count"],
                                   y=ma.total_counts(normalized_events)["action_type"])),

        # side by side pie charts drilling into specifics of outgoing likes
        dmc.Text("Outgoing Likes You've Sent", size="xl", align="center", weight=500),
        dmc.Text("This is a deep dive into your outgoing likes. The pie chart on the left shows a breakdown of the rare"
                 " cases where Hinge shows you a users you have already sent an outgoing like to vs the users you liked"
                 " once. The pie chart on the right shows how many outgoing likes you sent where you left a comment on the"
                 " other person's profile.", align="center"),
        html.Div(className='row', children=[
            html.Div(className='six columns', children=[
        dcc.Graph(figure=px.pie(ma.analyze_double_likes(normalized_events), values="Count", names="Like Frequency",
                                title="Number of Outgoing Likes per Person"),
                  style={'width': '50%', 'display': 'inline-block'}),
        dcc.Graph(figure=px.pie(ma.like_comment_ratios(normalized_events), values="Count", names="Likes With/ Without "
                                                                                                 "Comments",
                                title="Outgoing Likes with Comments"),
                  style={'width': '50%', 'display': 'inline-block'}
                  )
            ]),
        ]),

        # table showing like comments
        dmc.Text("What You're Commenting When You Like Someone's Content", size="md", align="left"),
        dash_table.DataTable(data=ma.commented_outgoing_likes(normalized_events).to_dict('records'), page_size=10,
                             style_cell={'textAlign': 'left'}),

        # line chart showing activity type frequencies by day
        dmc.Text("Frequency of Action Types by Day", size="xl", align="center", weight=500),
        dmc.Text("This line graph displays the counts of each action type (likes, matches, chats, and blocks aka unmatches)"
                 " per day over the duration of time you have been on Hinge. The legend on the right lists each of the"
                 " different action types, and you can select/ unselect different types to look at particular ones.",
                 align="center"),
        dcc.Graph(figure=px.line(ma.activity_by_date(normalized_events),
                                 x=ma.activity_by_date(normalized_events)['activity_date'],
                                 y=ma.activity_by_date(normalized_events)['count'],
                                 color=ma.activity_by_date(normalized_events)['type'])),

        # pie chart showing percentage of interactions with a phone number share
        dmc.Text("How Many People Did You Give Your Number To?", size="xl", align="center", weight=500),
        dmc.Text("This is the ratio of people you shared your phone number with out of the total number of people you "
                 "had chats with. This operates on the assumption you gave your phone number in a standard format, "
                 "ex: XXX-XXX-XXXX, XXXXXXXXXX, or (XXX)XXX-XXXX.",
                 align="center"),
        dcc.Graph(figure=px.pie(ma.phone_number_shares(normalized_events), values="Count", names="Message Outcomes")),

        # histogram showing the number of outgoing messages in each chat
        dmc.Text("Outgoing Messages Sent per Chat", size="xl", align="center", weight=500),
        dmc.Text("This histogram shows the number of outgoing messages you sent in each chat.",
                 align="center"),
        dcc.Graph(figure=px.histogram(ma.date_count_distribution(normalized_events), x='outgoing_messages', nbins=50)
                  .update_layout(bargap=0.2)),
    ])


@callback(
    Output('javascript', 'run'),
    [Input('refresh-page', 'n_clicks')])
def refresh_button_clicked(data):
    if data is not None:
        reload_global_norm_events()
        return "location.reload();"
    return ''


# assign the layout to the layout variable defined above
layout = serve_layout()
