import json
import pandas as pd


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
