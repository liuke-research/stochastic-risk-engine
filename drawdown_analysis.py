import pandas as pd
import numpy as np



class DrawdownAnalyzer:


    def __init__(
        self,
        price_file,
        risk_file
    ):


        # =====================
        # load price
        # =====================

        self.price = pd.read_csv(
            price_file
        )


        self.price["date"] = pd.to_datetime(
            self.price["date"]
        )


        self.price = self.price.sort_values(
            "date"
        )



        # =====================
        # load risk
        # =====================

        self.risk = pd.read_csv(
            risk_file
        )


        self.risk["date"] = pd.to_datetime(
            self.risk["date"]
        )


        self.risk = self.risk.sort_values(
            "date"
        )



    # =====================
    # future return
    # =====================

    def future_return(
        self,
        date,
        horizon=60
    ):


        future = self.price[
            self.price["date"] >= date
        ]


        future = future.iloc[
            :horizon+1
        ]


        if len(future) < horizon:

            return np.nan



        p0 = future.iloc[0]["close"]

        p1 = future.iloc[-1]["close"]


        return (
            p1 / p0 - 1
        )



    # =====================
    # future maximum drawdown
    # =====================

    def future_drawdown(
        self,
        date,
        horizon=60
    ):


        future = self.price[
            self.price["date"] >= date
        ]


        future = future.iloc[
            :horizon+1
        ]


        if len(future)==0:

            return np.nan, None



        prices = future["close"].values


        dates = future["date"].values



        # historical maximum after signal

        peak = prices[0]


        max_dd = 0

        dd_date = dates[0]



        for i,p in enumerate(prices):


            if p > peak:

                peak = p


            dd = (
                p / peak - 1
            )


            if dd < max_dd:

                max_dd = dd

                dd_date = dates[i]



        return (
            max_dd,
            dd_date
        )



    # =====================
    # event analysis
    # =====================

    def analyze_events(
        self,
        events
    ):


        results = []



        for name,start,end in events:


            period = self.risk[

                (self.risk["date"] >= start)

                &

                (self.risk["date"] <= end)

            ]



            peak = period.loc[

                period["tail_risk"].idxmax()

            ]



            future_ret = self.future_return(

                peak["date"],

                horizon=60

            )



            max_dd, dd_date = self.future_drawdown(

                peak["date"],

                horizon=60

            )



            results.append(

                {


                    "Event":

                    name,



                    "Risk Peak Date":

                    peak["date"].strftime(
                        "%Y-%m-%d"
                    ),



                    "Tail Risk":

                    round(
                        peak["tail_risk"],
                        4
                    ),



                    "Next 60D Return (%)":

                    round(
                        future_ret*100,
                        2
                    ),



                    "Max Drawdown 60D (%)":

                    round(
                        max_dd*100,
                        2
                    ),



                    "Drawdown Date":

                    pd.to_datetime(
                        dd_date
                    ).strftime(
                        "%Y-%m-%d"
                    )

                }

            )



        return pd.DataFrame(results)





if __name__ == "__main__":


    analyzer = DrawdownAnalyzer(

        "data/HS300.csv",

        "HS300_risk_series.csv"

    )



    events = [


        (
            "2015 Market Crash",
            "2015-06-01",
            "2015-09-30"
        ),



        (
            "COVID Shock",
            "2020-02-01",
            "2020-04-30"
        ),



        (
            "2022 Downturn",
            "2022-03-01",
            "2022-05-31"
        )

    ]



    result = analyzer.analyze_events(
        events
    )



    print(
        "\n===== Risk Signal Validation =====\n"
    )


    print(
        result.to_string(
            index=False
        )
    )


    result.to_csv(
        "risk_signal_validation.csv",
        index=False
    )