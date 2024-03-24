from dash import html
import dash_mantine_components as dmc
from dash import dcc, dash_table, Input, Output, State, callback
import plotly.express as px
import visdcc
from dash.exceptions import PreventUpdate

import src.match_analytics as ma

# TODO: open question, how do we cause a reload of the data when the user uploads a new file?
# normalized_events = ma.load_match_data("../data/mocked_data/matches.json")
# print(f"mocked events size: {normalized_events.size}")

global normalized_events


def setup_global_norm_events(path="../data/app_uploaded_files/matches.json"):
    global normalized_events
    # set fresh events with data from the uploads file
    normalized_events = ma.load_match_data(path)
    print(f"young fresh events size: {normalized_events.size}")


def get_global_norm_events():
    return normalized_events


# TODO: what's happening is when the Refresh Page button is clicked, reload_global_norm_events() is called which changes
# TODO: the value of normalized_events, but the layout is not being re-rendered with the new data.
def serve_layout():
    return html.Div([
        # visdcc.Run_js('javascript'),
        html.Button('Refresh Page', id='refresh-page', style={"fontSize": 16, 'font-family': "Open Sans, verdana, arial, sans-serif"}),
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
            # dcc.Interval(
            #     id='interval-component',
            #     interval=1 * 1000,  # in milliseconds
            #     n_intervals=0
            # )
        ]),
        # dcc.Graph(id='live-update-graph', figure={'data': [px.funnel(ma.total_counts(normalized_events), x=ma.total_counts(normalized_events)["count"],
        #                            y=ma.total_counts(normalized_events)["action_type"])]}),
        # dcc.Graph(id='live-update-graph',
        #           figure=px.funnel(ma.total_counts(normalized_events), x=ma.total_counts(normalized_events)["count"],
        #                            y=ma.total_counts(normalized_events)["action_type"])),

        # side by side pie charts drilling into specifics of outgoing likes
        dmc.Text("Outgoing Likes You've Sent", size="xl", align="center", weight=500),
        dmc.Text("This is a deep dive into your outgoing likes. The pie chart on the left shows a breakdown of the rare"
                 " cases where Hinge shows you a users you have already sent an outgoing like to vs the users you liked"
                 " once. The pie chart on the right shows how many outgoing likes you sent where you left a comment on the"
                 " other person's profile.", align="center"),
        # html.Div(className='row', children=[
        #     html.Div(className='six columns', children=[
        # dcc.Graph(figure=px.pie(ma.analyze_double_likes(normalized_events), values="Count", names="Like Frequency",
        #                         title="Number of Outgoing Likes per Person"),
        #           style={'width': '50%', 'display': 'inline-block'}),
        # dcc.Graph(figure=px.pie(ma.like_comment_ratios(normalized_events), values="Count", names="Likes With/ Without "
        #                                                                                          "Comments",
        #                         title="Outgoing Likes with Comments"),
        #           style={'width': '50%', 'display': 'inline-block'}
        #           )
        #     ]),
        # ]),

        # table showing like comments
        dmc.Text("What You're Commenting When You Like Someone's Content", size="md", align="left"),
        # dash_table.DataTable(data=ma.commented_outgoing_likes(normalized_events).to_dict('records'), page_size=10,
        #                      style_cell={'textAlign': 'left'}),

        # line chart showing activity type frequencies by day
        dmc.Text("Frequency of Action Types by Day", size="xl", align="center", weight=500),
        dmc.Text("This line graph displays the counts of each action type (likes, matches, chats, and blocks aka unmatches)"
                 " per day over the duration of time you have been on Hinge. The legend on the right lists each of the"
                 " different action types, and you can select/ unselect different types to look at particular ones.",
                 align="center"),
        # dcc.Graph(figure=px.line(ma.activity_by_date(normalized_events),
        #                          x=ma.activity_by_date(normalized_events)['activity_date'],
        #                          y=ma.activity_by_date(normalized_events)['count'],
        #                          color=ma.activity_by_date(normalized_events)['type'])),

        # pie chart showing percentage of interactions with a phone number share
        dmc.Text("How Many People Did You Give Your Number To?", size="xl", align="center", weight=500),
        dmc.Text("This is the ratio of people you shared your phone number with out of the total number of people you "
                 "had chats with. This operates on the assumption you gave your phone number in a standard format, "
                 "ex: XXX-XXX-XXXX, XXXXXXXXXX, or (XXX)XXX-XXXX.",
                 align="center"),
        # dcc.Graph(figure=px.pie(ma.phone_number_shares(normalized_events), values="Count", names="Message Outcomes")),

        # histogram showing the number of outgoing messages in each chat
        dmc.Text("Outgoing Messages Sent per Chat", size="xl", align="center", weight=500),
        dmc.Text("This histogram shows the number of outgoing messages you sent in each chat.",
                 align="center"),
        # dcc.Graph(figure=px.histogram(ma.date_count_distribution(normalized_events), x='outgoing_messages', nbins=50)
        #           .update_layout(bargap=0.2)),
    ])


# @callback(
#     Output('javascript', 'run'),
#     [Input('refresh-page', 'n_clicks')]
# )
# def refresh_button_clicked(data):
#     if data is not None:
#         reload_global_norm_events()
#         # TODO: do we need this?
#         # this part is responsible for reloading the page
#         return "location.reload();"
#     return ''


@callback(
    Output('live-update-graph', 'figure'),
    [Input('refresh-page', 'n_clicks')]
)
def update_graph_live(data):
    if data is None:
        raise PreventUpdate
    # elif data is not None:
        # reload_global_norm_events()
        # fresh_events = get_global_norm_events()
        # print(f"inside update_graph_live, fresh events: {fresh_events.size}")
        # figure = px.funnel(ma.total_counts(fresh_events), x=ma.total_counts(fresh_events)["count"],
        #                            y=ma.total_counts(fresh_events)["action_type"])

    setup_global_norm_events()
    df = px.data.iris()  # iris is a pandas DataFrame
    figure = px.scatter(df, x="sepal_width", y="sepal_length")

    return figure
        # return {'data': [px.funnel(ma.total_counts(fresh_events), x=ma.total_counts(fresh_events)["count"],
        #                            y=ma.total_counts(fresh_events)["action_type"])]}
        # return dcc.Graph(
        #              figure=px.funnel(ma.total_counts(fresh_events), x=ma.total_counts(fresh_events)["count"],
        #                            y=ma.total_counts(fresh_events)["action_type"])
        #              )


# assign the layout to the layout variable defined above
layout = serve_layout()
