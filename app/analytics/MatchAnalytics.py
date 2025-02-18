import pandas as pd
import re
import json


def prepare_uploaded_match_data(file_path="../data/app_uploaded_files/matches.json"):
    __validate_upload_file_type(file_path)
    __validate_match_file_upload(file_path)

    with open(file_path, 'r') as file:
        # match upload data is a list of dictionaries
        match_upload_data = json.load(file)

    events = []
    for interaction, all_actions in enumerate(match_upload_data):
        # action type is like, match, chats, blocks, overarching "action"
        for action_type, actions in all_actions.items():
            # action is the metadata assoc. one event of the action type
            for action in actions:
                action["interaction_id"] = interaction
                events.append(action)

    return pd.DataFrame(events).sort_values("timestamp")


def date_count_distribution(events):
    chat_events = events[events["type"] == "chats"]
    chats_per_interaction = chat_events.groupby('interaction_id').size()

    # convert the Series to a DataFrame with specified column names, have to reset the index
    interaction_counts = chats_per_interaction.to_frame().reset_index()
    interaction_counts.columns = ['interaction_id', 'outgoing_messages']
    return interaction_counts


def activity_by_date(events):
    events['activity_date'] = pd.DatetimeIndex(events["timestamp"]).date

    event_type_counts_by_date = events.groupby(['activity_date', 'type']).size()

    # creating a DataFrame from the Series, have to reset the index
    action_type_freq_per_day = pd.DataFrame(event_type_counts_by_date).reset_index()
    action_type_freq_per_day.columns = ['activity_date', 'type', 'count']

    return action_type_freq_per_day


def analyze_double_likes(events):
    like_events = events[events["type"] == "like"]
    multi_like_event_count = len(like_events.groupby('interaction_id').filter(lambda x: len(x) > 1))
    single_like_event_count = len(like_events) - multi_like_event_count

    single_vs_double_likes = pd.DataFrame(
        [['Single Like', single_like_event_count], ['Multiple Likes', multi_like_event_count]],
        columns=["Like Frequency", "Count"])

    return single_vs_double_likes


def total_counts(events):
    distinct_interaction_count = len(pd.unique(events['interaction_id']))
    like_event_count = len(events[events['type'] == "like"])
    match_event_count = len(events[events['type'] == "match"])

    chat_events = events[events['type'] == "chats"]
    chat_event_count = len(chat_events.interaction_id.unique())

    totals = pd.DataFrame(
        [['Distinct Interactions', distinct_interaction_count], ['Outgoing Likes', like_event_count],
         ['Matches', match_event_count],
         ['Chats', chat_event_count]],
        columns=["action_type", "count"])
    return totals


def commented_outgoing_likes(events):
    likes_w_comments = __build_comments_list(events)

    return pd.DataFrame(likes_w_comments, columns=["Comments"])


def like_comment_ratios(events):
    likes_w_comments = __build_comments_list(events)
    likes_wo_comment = len(events) - len(likes_w_comments)

    likes_w_wo_comments = pd.DataFrame(
        [['Likes with Comments', len(likes_w_comments)], ['Likes without Comments', likes_wo_comment]],
        columns=["Likes With/ Without Comments", "Count"])
    return likes_w_wo_comments


def phone_number_shares(events):
    chats_w_messages = events.where(events["type"] == "chats")
    chats_w_messages = chats_w_messages[chats_w_messages['body'].notna()]
    total_messages_w_chats = len(chats_w_messages)

    message_bodies = chats_w_messages['body']

    phone_number_shared = []
    for message in message_bodies:
        # finds common phone number formats in the message: XXX-XXX-XXXX, XXX.XXX.XXXX, (XXX) XXX-XXXX
        message_containing_number = re.findall(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}", message)

        if len(message_containing_number) >= 1:
            phone_number_shared.append(message_containing_number)

    phone_number_share_ratios = pd.DataFrame([['Gave Phone Number', len(phone_number_shared)],
                                              ['Did Not Give Phone Number', total_messages_w_chats]],
                                             columns=["Message Outcomes", "Count"])
    return phone_number_share_ratios

def __build_comments_list(events):
    likes_w_comments = []
    like_events = events["like"].dropna()
    for value in like_events:
        # likes are an array with a single element (most of the time)
        # TODO: handle multiple likes, it's rare but possible
        like_event = value[0]
        if like_event.get('comment') is not None:
            likes_w_comments.append(like_event.get('comment'))

    return likes_w_comments


def __validate_upload_file_type(file_path):
    if not file_path.endswith('.json'):
        raise ValueError("Invalid file type. Please upload a JSON file.")


def __validate_match_file_upload(file_path):
    if 'match' not in file_path:
        raise ValueError("Invalid file name. Please upload a file with 'match' in the file name.")
