import pandas as pd


class Events:
    def __init__(self):
        self.data_frame = pd.DataFrame()

    def set_data_frame(self, data_frame):
        if isinstance(data_frame, pd.DataFrame):
            self.data_frame = data_frame
        else:
            raise ValueError("Input must be a DataFrame")

    def get_data_frame(self):
        return self.data_frame


