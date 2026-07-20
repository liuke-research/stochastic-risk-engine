import numpy as np
import pandas as pd

from features.state_embedding import StateEmbedding

from core_math.harris_ergodicity import HarrisErgodicity
from core_math.rpf_operator import RPFOperator
from core_math.dv_ldp_solver import DVLDPSolver

from quant_signals.tail_risk_index import TailRiskIndex



class RollingRiskEngine:


    def __init__(
        self,
        window=250
    ):

        self.window = window

        self.embedder = StateEmbedding()

        self.harris = HarrisErgodicity()

        self.rpf = RPFOperator()

        self.dv = DVLDPSolver()

        self.risk = TailRiskIndex()



    def run(
        self,
        returns,
        dates,
        step=20
    ):


        results = []


        for count, i in enumerate(
            range(
                self.window,
                len(returns),
                step
            )
        ):


            if count % 10 == 0:

                print(
                    f"Rolling progress: {count}"
                )


            # =====================
            # rolling market window
            # =====================

            window_returns = returns[
                i-self.window:i
            ]


            date = dates[i]



            # =====================
            # state embedding
            # =====================

            states = self.embedder.transform(
                window_returns,
                window=20
            )


            if len(states) < 50:

                continue



            # =====================
            # Harris recovery
            # =====================

            mixing_rate = (
                self.harris
                .compute_mixing_rate(states)
            )


            half_life = (
                np.log(2)
                /
                mixing_rate
            )



            # =====================
            # spectral gap
            # =====================

            eigvals, gap = (
                self.rpf
                .spectral_gap(states)
            )



            # =====================
            # DV tail risk
            # =====================

            dv_rate = (
                self.dv
                .rate_function(states)
            )



            # =====================
            # Tail Risk Index
            # =====================

            tail_risk = (
                self.risk
                .compute(
                    dv_rate,
                    gap
                )
            )



            results.append(
                [
                    date,
                    mixing_rate,
                    half_life,
                    gap,
                    dv_rate,
                    tail_risk
                ]
            )



        return pd.DataFrame(
            results,
            columns=[
                "date",
                "mixing_rate",
                "half_life",
                "spectral_gap",
                "dv_rate",
                "tail_risk"
            ]
        )