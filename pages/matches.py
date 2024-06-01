from dash import html
import dash_mantine_components as dmc
from dash import dcc, dash_table, Input, Output, callback
import plotly.express as px
from dash.exceptions import PreventUpdate

import analytics


global normalized_events


def serve_layout():
    return html.Div([
        html.Button('Reload Graphs', id='refresh-page', style={"fontSize": 16, 'font-family': "Open Sans, verdana, arial, sans-serif"}),
        dmc.Space(h=20),

        dmc.Text("Match Analytics", style={"fontSize": 28}, weight=500),
        dmc.Text("This section contains insights about the interactions (likes, matches, chats, and unmatches) you've "
                 "had on Hinge."),
        dmc.Space(h=20),

        # funnel graph showing breakdown of interactions
        dmc.Text("Interaction Funnel", size="xl", align="center", weight=500),
        dmc.Text("This funnel represents the funnel of your interactions with people on Hinge. The outermost layer "
                 "represents the total number of people you interacted with. Then it shows the number of outgoing likes "
                 "you sent, matches received, and conversations started from those matches.", align="center"),
        html.Div([
            dcc.Graph(id='live-update-graph'),
        ]),

        # side by side pie charts drilling into specifics of outgoing likes
        dmc.Text("Outgoing Likes You've Sent", size="xl", align="center", weight=500),
        dmc.Text("This is a deep dive into your outgoing likes. The pie chart on the left shows a breakdown of the rare"
                 " cases where Hinge shows you a users you have already sent an outgoing like to vs the users you liked"
                 " once. The pie chart on the right shows how many outgoing likes you sent where you left a comment on the"
                 " other person's profile.", align="center"),
        html.Div(className='row', children=[
            html.Div(className='six columns', children=[
            dcc.Graph(id="live-update-double-likes-graph", style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(id="live-update-commented-likes-graph", style={'width': '50%', 'display': 'inline-block'})
            ]),
        ]),

        # table showing like comments
        dmc.Text("What You're Commenting When You Like Someone's Content", size="xl", align="center", weight=500),
        html.Div([
            dash_table.DataTable(id='datatable-interactivity'),
            html.Div(id='datatable-interactivity-container'),
        ]),

        # line chart showing activity type frequencies by day
        dmc.Text("Frequency of Action Types by Day", size="xl", align="center", weight=500),
        dmc.Text("This line graph displays the counts of each action type (likes, matches, chats, and blocks aka unmatches)"
                 " per day over the duration of time you have been on Hinge. The legend on the right lists each of the"
                 " different action types, and you can select/ unselect different types to look at particular ones.",
                 align="center"),
        dcc.Graph("live-update-action_types-graph"),

        # pie chart showing percentage of interactions with a phone number share
        dmc.Text("How Many People Did You Give Your Number To?", size="xl", align="center", weight=500),
        dmc.Text("This is the ratio of people you shared your phone number with out of the total number of people you "
                 "had chats with. This operates on the assumption you gave your phone number in a standard format, "
                 "ex: XXX-XXX-XXXX, XXXXXXXXXX, or (XXX)XXX-XXXX.",
                 align="center"),
        dcc.Graph("live-update-number_shares-graph"),

        # histogram showing the number of outgoing messages in each chat
        dmc.Text("Outgoing Messages Sent per Chat", size="xl", align="center", weight=500),
        dmc.Text("This histogram shows the number of outgoing messages you sent in each chat.",
                 align="center"),
        dcc.Graph("live-update-messages-per-chat-graph"),
    ])


@callback(
    Output('live-update-graph', 'figure'),
    [Input('refresh-page', 'n_clicks')]
)
def update_graph_live(data):
    __check_for_live_update_data(data)
    __setup_global_norm_events()
    return px.funnel(analytics.total_counts(normalized_events), x=analytics.total_counts(normalized_events)["count"],
                               y=analytics.total_counts(normalized_events)["action_type"])


@callback(
    Output('live-update-double-likes-graph', 'figure'),
    [Input('refresh-page', 'n_clicks')]
)
def update_double_likes_pie(data):
    __check_for_live_update_data(data)
    __setup_global_norm_events()
    return px.pie(analytics.analyze_double_likes(normalized_events), values="Count", names="Like Frequency",
                                title="Number of Outgoing Likes per Person")


@callback(
    Output('live-update-commented-likes-graph', 'figure'),
    [Input('refresh-page', 'n_clicks')]
)
def update_commented_likes_pie(data):
    __check_for_live_update_data(data)
    __setup_global_norm_events()
    return px.pie(analytics.like_comment_ratios(normalized_events), values="Count", names="Likes With/ Without Comments",
                                title="Outgoing Likes with Comments")


@callback(
    Output('live-update-action_types-graph', 'figure'),
    [Input('refresh-page', 'n_clicks')]
)
def update_action_types_graph(data):
    __check_for_live_update_data(data)
    __setup_global_norm_events()
    return px.line(analytics.activity_by_date(normalized_events),
                             x=analytics.activity_by_date(normalized_events)['activity_date'],
                             y=analytics.activity_by_date(normalized_events)['count'],
                             color=analytics.activity_by_date(normalized_events)['type'],
                             labels={'x': 'activity_date', 'y': 'count'})


@callback(
    Output('live-update-number_shares-graph', 'figure'),
    [Input('refresh-page', 'n_clicks')]
)
def update_number_shares_graph(data):
    __check_for_live_update_data(data)
    __setup_global_norm_events()
    return px.pie(analytics.phone_number_shares(normalized_events), values="Count", names="Message Outcomes")


@callback(
    Output('live-update-messages-per-chat-graph', 'figure'),
    [Input('refresh-page', 'n_clicks')]
)
def update_messages_per_chat_graph(data):
    __check_for_live_update_data(data)
    __setup_global_norm_events()
    return px.histogram(analytics.date_count_distribution(normalized_events), x='outgoing_messages', nbins=50).update_layout(bargap=0.2)


@callback(
    Output('datatable-interactivity-container', 'children'),
    [Input('refresh-page', 'n_clicks')]
)
def update_comment_table(data):
    __check_for_live_update_data(data)
    __setup_global_norm_events()
    commented_outgoing_likes_data = analytics.commented_outgoing_likes(normalized_events).to_dict('records')
    return [
        dash_table.DataTable(data=commented_outgoing_likes_data, page_size=10,
                             style_cell={'textAlign': 'left'})
       ]


layout = serve_layout()


def __setup_global_norm_events(file_path="../data/app_uploaded_files/matches.json"):
    global normalized_events
    normalized_events = analytics.prepare_uploaded_match_data(file_path)


def __check_for_live_update_data(data):
    if data is None:
        raise PreventUpdate
