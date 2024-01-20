"""
Hinge Data Analysis
"""
__author__ = "Shelby Potts"
__version__ = "0.0.0"

import json
import pandas as pd
import plotly.express as px
from dash import Dash, html, dash_table, dcc
import dash_mantine_components as dmc

# Initialize the app - incorporate a Dash Mantine theme
external_stylesheets = [dmc.theme.DEFAULT_COLORS]
app = Dash(__name__, external_stylesheets=external_stylesheets)


def load_match_data():
    """
    Loads the matches.json file provided by Hinge through the Data Export request
    :return: a DataFrame of normalized match event data
    """
    json_file_path = 'data/export/matches.json'

    # opening json file
    with open(json_file_path, 'r') as file:
        # raw data is a list of dictionaries "list of interactions with a person"
        raw_data = json.load(file)

    events = []
    for interaction, all_actions in enumerate(raw_data):
        # action type is like, match, chats, blocks, overarching "action"
        for action_type, actions in all_actions.items():
            # action is the metadata assoc. one event of the action type
            for action in actions:
                action["interaction_id"] = interaction
                events.append(action)

    return pd.DataFrame(events).sort_values("timestamp")


def total_counts(df):
    """
    Counts the total number of occurrences for each action_type.
    :param df: the DataFrame to analyze
    :return: a DataFrame of total count of occurrences for each action type
    """
    # get counts of each of the different action types
    distinct_interactions = len(pd.unique(df['interaction_id']))
    like_count = len(df[df['type'] == "like"])
    match_count = len(df[df['type'] == "match"])

    # get distinct ids for events with chats, so it doesn't count every message in the interaction
    chats_df = df[df['type'] == "chats"]
    chat_count = len(chats_df.interaction_id.unique())

    # NOTE: taking unmatches out for now...
    # TODO: figure out if you want to keep this or get rid of it, but it looks like trash in the funnel
    block_count = len(df[df['type'] == "block"])

    # build a DataFrame with the total counts
    totals = pd.DataFrame([['Distinct Interactions', distinct_interactions], ['Outgoing Likes', like_count], ['Matches', match_count], ['Chats', chat_count]],
                          columns=["Action Type", "Count"])
    return totals


def analyze_double_likes(df):
    # grab 'like' events
    likes_df = df[df["type"] == "like"]
    # get likes where the count of times you liked that person are +1
    multi_likes = likes_df.groupby('interaction_id').filter(lambda x: len(x) > 1)

    # singles likes as the total minus the count of people who were liked more than once
    single_likes = len(likes_df) - len(multi_likes)

    # build a DataFrame with the breakdown of outgoing likes
    single_vs_double_likes = pd.DataFrame(
        [['Single Likes', single_likes], ['Multiple Likes', len(multi_likes)]],
        columns=["Like Frequency", "Count"])

    return single_vs_double_likes


def analyze_outgoing_likes(df):
    likes_w_comments = []
    likes = df["like"].dropna()
    for value in likes:
        record = value[0]
        if record.get('comment') is not None:
            likes_w_comments.append(record.get('comment'))
    likes_wo_comment = len(df) - len(likes_w_comments)

    # build a DataFrame with the breakdown of outgoing likes
    likes_w_wo_comments = pd.DataFrame(
        [['Likes With Comments', len(likes_w_comments)], ['Likes Without Comments', likes_wo_comment]],
        columns=["Likes With/ Without Comments", "Count"])

    return likes_w_wo_comments


def outgoing_messages(df):
    """
    Captures the outgoing messages sent.
    :param df: the DataFrame to analyze
    :return: a DataFrame with outgoing messages
    """
    # creating a filter to use in the where clause
    where_clause = df["type"] == "chats"

    # filtering data to just chat events that have messages
    chats_w_messages = df.where(where_clause)
    chats_w_messages = chats_w_messages[chats_w_messages['body'].notna()]
    print(chats_w_messages)

    return chats_w_messages


# capture the normalized_events
normalized_events = load_match_data()
# persist DataFrame with total counts
totals_df = total_counts(normalized_events)
# get the breakdown of single vs double likes given just the normalized events that are 'likes'
like_freq_df = analyze_double_likes(normalized_events[normalized_events["type"] == "like"])
# counts of likes with and without comments
like_w_wo_comments_df = analyze_outgoing_likes(normalized_events)

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

