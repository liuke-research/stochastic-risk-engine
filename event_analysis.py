import pandas as pd


class EventAnalyzer:


    def __init__(
        self,
        risk_file
    ):

        self.df = pd.read_csv(
            risk_file
        )


        self.df["date"] = pd.to_datetime(
            self.df["date"]
        )


        self.df = self.df.sort_values(
            "date"
        )



    def analyze(
        self,
        name,
        start,
        end
    ):


        start = pd.to_datetime(
            start
        )

        end = pd.to_datetime(
            end
        )


        period = self.df[
            (self.df["date"] >= start)
            &
            (self.df["date"] <= end)
        ]


        if len(period)==0:

            return None



        # 最大风险点

        max_row = period.loc[
            period["tail_risk"].idxmax()
        ]



        return {

            "Event": name,

            "Max Tail Risk":
                round(
                    max_row["tail_risk"],
                    4
                ),

            "Peak Date":
                max_row["date"].strftime(
                    "%Y-%m-%d"
                ),

            "Half-life(days)":
                round(
                    max_row["half_life"],
                    2
                ),

            "Spectral Gap":
                round(
                    max_row["spectral_gap"],
                    4
                )
        }



if __name__ == "__main__":


    analyzer = EventAnalyzer(
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



    results = []


    for event in events:

        result = analyzer.analyze(
            event[0],
            event[1],
            event[2]
        )

        results.append(
            result
        )



    result_df = pd.DataFrame(
        results
    )


    print(
        "\n===== Historical Stress Test =====\n"
    )


    print(
        result_df.to_string(
            index=False
        )
    )


    result_df.to_csv(
        "stress_test_results.csv",
        index=False
    )