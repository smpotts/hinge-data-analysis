import json
import pandas as pd
from pathlib import Path
import requests


def load_match_data(file_path='data/export/matches.json'):
    """
    Loads the matches.json file provided by Hinge through the Data Export request
    :return: a DataFrame of normalized match event data
    """
    json_file_path = file_path

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


def liked_photos(df):
    """
    In a recent data export from Hinge, they started including the urls of the liked photos in the content metadata.
    This retrieves the url metadata.
    :param df: DataFrame of normalized events
    """
    # create a folder for liked photos if it does not exist already
    Path("data/liked_photos").mkdir(parents=True, exist_ok=True)

    # get events that have content metadata
    content = df["content"].dropna()
    # extract the urls from the content metadata
    urls = []
    for record in content:
        json_data = json.loads(record)
        url = json_data[0]["photo"]["url"]
        if len(url) > 1:
            # add to a list
            urls.append(url)

    counter = 0
    for photo_url in urls:
        # send a GET request to the URL
        response = requests.get(photo_url)

        # check if the request was successful (status code 200)
        if response.status_code == 200:
            # get the content of the response (photo binary data)
            photo_content = response.content

            # save the photo to a local file
            file_name = "{}{}{}".format("data/liked_photos/liked_photo_", counter, ".jpg")
            with open(file_name, "wb") as file:
                file.write(photo_content)

            print("Photo downloaded successfully.")
        else:
            print(f"Failed to download photo. Status code: {response.status_code}")
        # increment counter
        counter = counter + 1
