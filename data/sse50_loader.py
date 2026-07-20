import pandas as pd
import numpy as np


class SSE50Loader:

    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):

        df = pd.read_csv(self.file_path)

        # 默认需要:
        # date, close

        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")

        price = df["close"].values

        returns = np.diff(
            np.log(price)
        )

        return returns