import pandas as pd
import numpy as np


class HS300Loader:


    def __init__(self, file_path):

        self.file_path = file_path



    def load(self):

        df = pd.read_csv(
            self.file_path
        )


        df["date"] = pd.to_datetime(
            df["date"]
        )


        df = df.sort_values(
            "date"
        )


        df = df[
            df["date"] <= "2025-12-31"
        ]


        prices = df["close"].values


        returns = np.diff(
            np.log(prices)
        )


        return returns



    def load_dates(self):

        df = pd.read_csv(
            self.file_path
        )


        df["date"] = pd.to_datetime(
            df["date"]
        )


        df = df.sort_values(
            "date"
        )


        df = df[
            df["date"] <= "2025-12-31"
        ]


        dates = df["date"].values[1:]


        return dates