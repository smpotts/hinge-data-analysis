class MatchAnalytics:
    @staticmethod
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

    @staticmethod
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
        totals = pd.DataFrame(
            [['Distinct Interactions', distinct_interactions], ['Outgoing Likes', like_count], ['Matches', match_count],
             ['Chats', chat_count]],
            columns=["Action Type", "Count"])
        return totals

    @staticmethod
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

    @staticmethod
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
