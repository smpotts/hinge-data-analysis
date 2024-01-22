import pandas as pd
import re


def activity_by_date(df):
    """
    Adds a date field to the normalized_events DataFrame and calculates counts of activity_type
    by day.
    :param df: a DataFrame of normalized events
    :return: a DataFrame containing counts for each activity_type by day
    """
    # add a new column that has the date the activity occurred
    df['activity_date'] = pd.DatetimeIndex(df["timestamp"]).date

    # get counts of each action type per day
    counts_by_date = df.groupby(['activity_date', 'type']).size()

    # create a DataFrame with the counts of action types per day
    action_type_freq_per_day = pd.DataFrame(counts_by_date).reset_index()
    action_type_freq_per_day.columns = ['activity_date', 'type', 'count']

    return action_type_freq_per_day


def analyze_double_likes(df):
    """
    Analyzes counts of people who have received just one like, and people who have received more than one outgoing like.
    :param df: a DataFrame of normalized events
    :return: a DataFrame with statistics about how many people have received one or more than one outgoing like
    """
    # grab 'like' events
    likes_df = df[df["type"] == "like"]
    # get likes where the count of times you liked that person are +1
    multi_likes = likes_df.groupby('interaction_id').filter(lambda x: len(x) > 1)

    # single likes as the total minus the count of people who were liked more than once
    single_likes = len(likes_df) - len(multi_likes)

    # build a DataFrame with the breakdown of outgoing likes
    single_vs_double_likes = pd.DataFrame(
        [['Single Like', single_likes], ['Multiple Likes', len(multi_likes)]],
        columns=["Like Frequency", "Count"])

    return single_vs_double_likes


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

    # build a DataFrame with the total counts
    totals = pd.DataFrame(
        [['Distinct Interactions', distinct_interactions], ['Outgoing Likes', like_count], ['Matches', match_count],
         ['Chats', chat_count]],
        columns=["action_type", "count"])
    return totals


def commented_outgoing_likes(df):
    # TODO: this part of the method is a duplicate of like_comment_ratios
    likes_w_comments = []
    likes = df["like"].dropna()
    for value in likes:
        record = value[0]
        if record.get('comment') is not None:
            likes_w_comments.append(record.get('comment'))

    return pd.DataFrame(likes_w_comments, columns=["Comments"])


def like_comment_ratios(df):
    """
    Gathers statistics about how many outgoing likes included a comment.
    :param df: a DataFrame of normalized events
    :return: a DataFrame with statistics about likes with and without comments
    """
    likes_w_comments = []
    likes = df["like"].dropna()
    for value in likes:
        record = value[0]
        if record.get('comment') is not None:
            likes_w_comments.append(record.get('comment'))
    likes_wo_comment = len(df) - len(likes_w_comments)

    likes_w_wo_comments = pd.DataFrame(
        [['Likes with Comments', len(likes_w_comments)], ['Likes without Comments', likes_wo_comment]],
        columns=["Likes With/ Without Comments", "Count"])
    return likes_w_wo_comments


def phone_number_shares(df):
    # creating a filter to use in the where clause
    where_clause = df["type"] == "chats"

    # filtering data to just chat events that have messages
    chats_w_messages = df.where(where_clause)
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

    number_shares = pd.DataFrame([['Gave Phone Number', len(gave_number)], ['Did Not Give Phone Number', total_chats]],
                                 columns=["Message Outcomes", "Count"])

    return number_shares
