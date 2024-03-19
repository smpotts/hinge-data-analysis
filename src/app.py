"""
Hinge Data Analysis
"""
__author__ = "Shelby Potts"
__version__ = "0.0.0"

import plotly.express as px
import dash_mantine_components as dmc
from flask import Flask
import dash
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
import os
import base64

import src.match_analytics as ma
import src.dash_elements as de
import src.data_utility as du
import src.user_analytics as ua


# define the directory where uploaded files will be stored
UPLOAD_DIRECTORY = "../data/app_uploaded_files"

# initialize the app - incorporate a Dash Mantine theme
external_stylesheets = [dmc.theme.DEFAULT_COLORS]
server = Flask(__name__)
app = Dash(__name__, server=server, use_pages=True, external_stylesheets=external_stylesheets)

####################
### Initialize Data
####################
# TODO: figure out where to put all this and uncomment it
# normalized_events = du.load_match_data()
# persist DataFrame with total counts
# totals_df = ma.total_counts(normalized_events)
# get the breakdown of single vs double likes given just the normalized events that are 'likes'
# like_freq_df = ma.analyze_double_likes(normalized_events)
# counts of likes with and without comments
# like_w_wo_comments_df = ma.like_comment_ratios(normalized_events)
# capture action types per day
# action_type_freq_per_day = ma.activity_by_date(normalized_events)
# get ratio of phone number shares
# number_shares = ma.phone_number_shares(normalized_events)
# save commented outgoing likes
# commented_likes = ma.commented_outgoing_likes(normalized_events)
# counts of message per chat
# chat_counts = ma.date_count_distribution(normalized_events)


# user latitude and longitude coordinates
# TODO: fix me...
# user_coords = ua.parse_user_ip_addresses()


app.layout = html.Div([
    # page title
    dmc.Title('Hinge Data Analysis', color="black", size="h1"),

    # informational info about the app
    de.INTRO_INFO,
    # section for uploading files
    de.UPLOAD_FILES,

    # shows links to the other pages
    dmc.Text("Data Insights", style={"fontSize": 28}, weight=500),
    dmc.Text("After uploading your data files, you can click on the page links below to see insights "
             "from the data provided by Hinge."),
    dmc.Space(h=10),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name'].title()}", href=page["relative_path"],
                     style={"fontSize": 20, 'font-family': "Open Sans, verdana, arial, sans-serif"})
        ) for page in dash.page_registry.values()
    ]),
    dmc.Space(h=20),

    # container for multi-page setup
    dash.page_container,

    ####################
    ### Data Insights Section
    ####################
    # TODO: figure out where to put all this and uncomment it
    # de.DATA_INSIGHTS_TEXT,

    # funnel graph showing breakdown of interactions
    # de.INTERACTION_FUNNEL_TEXT,
    # dcc.Graph(figure=px.funnel(totals_df, x=totals_df["count"], y=totals_df["action_type"])),

    # side by side pie charts drilling into specifics of outgoing likes
    # de.OUTGOING_LIKES_TEXT,
    # html.Div(className='row', children=[
    #     html.Div(className='six columns', children=[
            # dcc.Graph(figure=px.pie(like_freq_df, values="Count", names="Like Frequency",
            #                         title="Number of Outgoing Likes per Person"),
            #           style={'width': '50%', 'display': 'inline-block'}),
            # dcc.Graph(figure=px.pie(like_w_wo_comments_df, values="Count", names="Likes With/ Without Comments",
            #                         title="Outgoing Likes with Comments"),
            #           style={'width': '50%', 'display': 'inline-block'}
            #           )
        # ]),
    # ]),

    # table showing like comments
    # dmc.Text("What You're Commenting When You Like Someone's Content", size="md", align="left"),
    # dash_table.DataTable(data=commented_likes.to_dict('records'), page_size=10, style_cell={'textAlign': 'left'}),

    # line chart showing activity type frequencies by day
    # de.ACTION_TYPE_FREQ
    # dcc.Graph(figure=px.line(action_type_freq_per_day, x=action_type_freq_per_day['activity_date'],
    #                          y=action_type_freq_per_day['count'],
    #                          color=action_type_freq_per_day['type'])),

    # pie chart showing percentage of interactions with a phone number share
    # de.NUMBER_SHARES,
    # dcc.Graph(figure=px.pie(number_shares, values="Count", names="Message Outcomes")),

    # histogram showing the number of outgoing messages in each chat
    # de.OUTGOING_MESSAGES,
    # dcc.Graph(figure=px.histogram(chat_counts, x='outgoing_messages', nbins=50).update_layout(bargap=0.2)),

    # TODO: figure out what to do with this map because it's god awful to run
    # de.GEO_LOCATION,
    # dcc.Graph(figure=px.scatter_geo(user_coords, locationmode="USA-states", lat="latitude", lon="longitude",
    #             projection="orthographic"))
])


def parse_contents(list_of_contents, list_of_names):
    """
    Decode and store a file uploaded with Plotly Dash.
    """
    # create the upload directory if it doesn't exist
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    for content, name in zip(list_of_contents, list_of_names):
        data = content.encode("utf8").split(b";base64,")[1]

        with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
            fp.write(base64.decodebytes(data))

        return html.Div([
            html.Div(
                dmc.Text(name, style={"fontSize": 16, 'font-family': "Open Sans, verdana, arial, sans-serif"})
            ) for name in list_of_names
        ])


@callback(Output('output-data-upload', 'children'),
          Input('upload-data', 'contents'),
          State('upload-data', 'filename'))
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(list_of_contents, list_of_names)]
        return children


if __name__ == '__main__':
    app.run(debug=True)