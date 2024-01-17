import json
import pdb

import pandas as pd


def normalize_match_data():
    """
    Loads the matches.json file provided by Hinge through the Data Export request
    :return: a DataFrame of normalized match event data
    """
    json_file_path = 'data/test.json'

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


def total_counts_by_action_type(df, action_type: str):
    """
    Counts total number of occurrences for a particular action_type.
    :param df: the DataFrame to analyze
    :param action_type: the specific action type to count
    :return: total count of occurrences
    """
    return (df["type"] == action_type).sum()


def total_messages_sent(df):
    """
    Total outgoing messages sent.
    :param df: the DataFrame to analyze.
    :return: the total number of outgoing messages sent
    """
    # creating a filter to use in the where clause
    where_clause = df["type"] == "chats"

    # filtering data to just chat events that have messages
    chats_w_messages = df.where(where_clause)
    chats_w_messages = chats_w_messages[chats_w_messages['body'].notna()]
    return len(chats_w_messages)


if __name__ == '__main__':
    normalized_events = normalize_match_data()
    print(normalized_events)
    total_messages_sent(normalized_events)

