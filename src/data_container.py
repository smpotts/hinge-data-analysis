import pandas as pd


global normalized_events
normalized_events = pd.DataFrame()


def set_normalized_events(norm):
    global normalized_events
    normalized_events = norm


def get_normalized_events():
    global normalized_events
    return normalized_events
