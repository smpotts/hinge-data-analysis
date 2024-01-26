import pandas as pd
import re


def date_count_distribution(events):
    """
    Captures how many outgoing messages were sent in each chat event.
    :param events: a DataFrame of normalized events
    :return: a DataFrame with counts of messages for each interaction
    """
    # grab 'chat' events
    chats_df = events[events["type"] == "chats"]

    # get counts of chats for each interaction
    chats_per_interaction = chats_df.groupby('interaction_id').size()

    # convert the Series to a DataFrame with specified column names, have to reset the index
    interaction_counts = chats_per_interaction.to_frame().reset_index()
    interaction_counts.columns = ['interaction_id', 'outgoing_messages']
    return interaction_counts


def activity_by_date(events):
    """
    Adds a date field to the normalized_events DataFrame and calculates counts of activity_type
    by day.
    :param events: a DataFrame of normalized events
    :return: a DataFrame containing counts for each activity_type by day
    """
    # add a new column that has the date the activity occurred
    events['activity_date'] = pd.DatetimeIndex(events["timestamp"]).date

    # get counts of each action type per day
    counts_by_date = events.groupby(['activity_date', 'type']).size()

    # create a DataFrame with the counts of action types per day
    action_type_freq_per_day = pd.DataFrame(counts_by_date).reset_index()
    action_type_freq_per_day.columns = ['activity_date', 'type', 'count']

    return action_type_freq_per_day


def analyze_double_likes(events):
    """
    Analyzes counts of people who have received just one like, and people who have received more than one outgoing like.
    :param events: a DataFrame of normalized events
    :return: a DataFrame with statistics about how many people have received one or more than one outgoing like
    """
    # grab 'like' events
    likes_df = events[events["type"] == "like"]
    # get likes where the count of times you liked that person are +1
    multi_likes = likes_df.groupby('interaction_id').filter(lambda x: len(x) > 1)

    # single likes as the total minus the count of people who were liked more than once
    single_likes = len(likes_df) - len(multi_likes)

    # build a DataFrame with the breakdown of outgoing likes
    single_vs_double_likes = pd.DataFrame(
        [['Single Like', single_likes], ['Multiple Likes', len(multi_likes)]],
        columns=["Like Frequency", "Count"])

    return single_vs_double_likes


def total_counts(events):
    """
    Counts the total number of occurrences for each action_type.
    :param events: a DataFrame of normalized events
    :return: a DataFrame of total count of occurrences for each action type
    """
    # get counts of each of the different action types
    distinct_interactions = len(pd.unique(events['interaction_id']))
    like_count = len(events[events['type'] == "like"])
    match_count = len(events[events['type'] == "match"])

    # get distinct ids for events with chats, so it doesn't count every message in the interaction
    chats_df = events[events['type'] == "chats"]
    chat_count = len(chats_df.interaction_id.unique())

    # build a DataFrame with the total counts
    totals = pd.DataFrame(
        [['Distinct Interactions', distinct_interactions], ['Outgoing Likes', like_count], ['Matches', match_count],
         ['Chats', chat_count]],
        columns=["action_type", "count"])
    return totals


def build_comments_list(events):
    """
    Helper method that extracts like events where there was an outgoing comment.
    :param events: a DataFrame with normalized events
    :return: a list of comments
    """
    likes_w_comments = []
    likes = events["like"].dropna()
    for value in likes:
        record = value[0]
        if record.get('comment') is not None:
            likes_w_comments.append(record.get('comment'))

    return likes_w_comments


def commented_outgoing_likes(events):
    """
    Creates a DataFrame containing like events where a comment was left.
    :param events: a DataFrame of normalized events
    :return: a DataFrame with like events where a comment was left
    """
    # grab like events with comments
    likes_w_comments = build_comments_list(events)

    return pd.DataFrame(likes_w_comments, columns=["Comments"])


def like_comment_ratios(events):
    """
    Gathers statistics about how many outgoing likes included a comment.
    :param events: a DataFrame of normalized events
    :return: a DataFrame with statistics about likes with and without comments
    """
    likes_w_comments = build_comments_list(events)
    likes_wo_comment = len(events) - len(likes_w_comments)

    likes_w_wo_comments = pd.DataFrame(
        [['Likes with Comments', len(likes_w_comments)], ['Likes without Comments', likes_wo_comment]],
        columns=["Likes With/ Without Comments", "Count"])
    return likes_w_wo_comments


def phone_number_shares(events):
    """
    Captures interactions where a phone number was shared.
    :param events: a DataFrame of normalized events
    :return: a DataFrame with ratios of phone number shares
    """
    # creating a filter to use in the where clause
    where_clause = events["type"] == "chats"

    # filtering data to just chat events that have messages
    chats_w_messages = events.where(where_clause)
    chats_w_messages = chats_w_messages[chats_w_messages['body'].notna()]
    total_chats = len(chats_w_messages)
    # outgoing_messages()
    body = chats_w_messages['body']

    gave_number = []
    for message in body:
        # uses a regular expression to find phone numbers in the message body
        result = re.findall(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}", message)

        # append the message to a list if there was a match in the result
        if len(result) >= 1:
            gave_number.append(result)

    # capture ratios of interactions with and without phone number shares
    number_shares = pd.DataFrame([['Gave Phone Number', len(gave_number)], ['Did Not Give Phone Number', total_chats]],
                                 columns=["Message Outcomes", "Count"])
    return number_shares
