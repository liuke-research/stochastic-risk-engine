import pandas as pd
import numpy as np


class MarketLoader:

    def __init__(self, file_path):

        self.file_path = file_path


    def load_returns(self):

        df = pd.read_csv(
            self.file_path
        )


        df["date"] = pd.to_datetime(
            df["date"]
        )

        df = df.sort_values(
            "date"
        )


        price = df["close"].values


        returns = np.diff(
            np.log(price)
        )


        return returns