from dash import html
import dash_mantine_components as dmc
from dash import dcc, dash_table, Input, Output, callback
import plotly.express as px
from dash.exceptions import PreventUpdate

import match_analytics as ma


global normalized_events


def setup_global_norm_events(path="../data/app_uploaded_files/matches.json"):
    global normalized_events
    # set fresh events with data from the uploads file
    normalized_events = ma.load_match_data(path)


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
    if data is None:
        raise PreventUpdate

    # initial setup of the global events
    setup_global_norm_events()
    # create the funnel graph
    figure = px.funnel(ma.total_counts(normalized_events), x=ma.total_counts(normalized_events)["count"],
                               y=ma.total_counts(normalized_events)["action_type"])
    return figure


@callback(
    Output('live-update-double-likes-graph', 'figure'),
    [Input('refresh-page', 'n_clicks')]
)
def update_double_likes_pie(data):
    if data is None:
        raise PreventUpdate
    setup_global_norm_events()
    # build the pie chart for double likes
    figure = px.pie(ma.analyze_double_likes(normalized_events), values="Count", names="Like Frequency",
                                title="Number of Outgoing Likes per Person")
    return figure


@callback(
    Output('live-update-commented-likes-graph', 'figure'),
    [Input('refresh-page', 'n_clicks')]
)
def update_commented_likes_pie(data):
    if data is None:
        raise PreventUpdate
    setup_global_norm_events()
    # build the pie chart for commented likes
    figure = px.pie(ma.like_comment_ratios(normalized_events), values="Count", names="Likes With/ Without Comments",
                                title="Outgoing Likes with Comments")
    return figure


@callback(
    Output('live-update-action_types-graph', 'figure'),
    [Input('refresh-page', 'n_clicks')]
)
def update_action_types_graph(data):
    if data is None:
        raise PreventUpdate
    setup_global_norm_events()
    # build the action types graph
    figure = px.line(ma.activity_by_date(normalized_events),
                             x=ma.activity_by_date(normalized_events)['activity_date'],
                             y=ma.activity_by_date(normalized_events)['count'],
                             color=ma.activity_by_date(normalized_events)['type'])
    return figure


@callback(
    Output('live-update-number_shares-graph', 'figure'),
    [Input('refresh-page', 'n_clicks')]
)
def update_number_shares_graph(data):
    if data is None:
        raise PreventUpdate
    setup_global_norm_events()
    # build the phone number shares graph
    figure = px.pie(ma.phone_number_shares(normalized_events), values="Count", names="Message Outcomes")
    return figure


@callback(
    Output('live-update-messages-per-chat-graph', 'figure'),
    [Input('refresh-page', 'n_clicks')]
)
def update_messages_per_chat_graph(data):
    if data is None:
        raise PreventUpdate
    setup_global_norm_events()
    # build the messages per chat graph
    figure = px.histogram(ma.date_count_distribution(normalized_events), x='outgoing_messages', nbins=50).update_layout(bargap=0.2)
    return figure


@callback(
    Output('datatable-interactivity-container', 'children'),
    [Input('refresh-page', 'n_clicks')]
)
def update_comment_table(data):
    # this prevents the page from throwing an error when trying to display the graphs before data is uploaded
    if data is None:
        raise PreventUpdate
    setup_global_norm_events()
    # build the messages per chat graph
    data = ma.commented_outgoing_likes(normalized_events).to_dict('records')
    return [
        dash_table.DataTable(data=data, page_size=10,
                             style_cell={'textAlign': 'left'})
       ]


# assign the layout to the layout variable defined above
layout = serve_layout()
