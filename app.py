"""
Hinge Data Analysis
"""
__author__ = "Shelby Potts"
__version__ = "0.0.0"

import json
import pandas as pd
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hinge_data_analysis():
    return 'Hinge Data Analysis'


def load_match_data():
    """
    Loads the matches.json file provided by Hinge through the Data Export request
    :return: a DataFrame of normalized match event data
    """
    json_file_path = 'data/test2.json'

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


def calculate_ratio(df, numerator: str, denominator: str, group_by=None):
    if group_by:
        pass
        # do a thing return a series
#             result = numerator.group_by(group_by) / denominator.group_by(group_by)
#             # TODO: return the result
#             pass
    else:
        return (df["type"] == numerator).sum() / (df["type"] == denominator).sum()


def total_counts(df):
    """
    Counts the total number of occurrences for each action_type.
    :param df: the DataFrame to analyze
    :return: a DataFrame of total count of occurrences for each action type
    """
    # get counts of each of the different action types
    chat_count = len(df[df['type'] == "chats"])
    match_count = len(df[df['type'] == "match"])
    like_count = len(df[df['type'] == "like"])
    block_count = len(df[df['type'] == "block"])
    distinct_interactions = len(pd.unique(df['interaction_id']))
    print(distinct_interactions)

    # build a DataFrame with the total counts
    totals = pd.DataFrame([['Likes', like_count], ['Matches', match_count], ['Outgoing Messages', chat_count], ['Blocks', block_count],
                           ['Distinct Interactions', distinct_interactions]],
                          columns=["Action Type", "Count"])
    return totals


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

    return chats_w_messages


if __name__ == '__main__':
    normalized_events = load_match_data()
    outgoing_messages(normalized_events)

