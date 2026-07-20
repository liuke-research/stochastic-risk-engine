import numpy as np


class TailRiskIndex:


    def compute(
        self,
        dv_rate,
        spectral_gap
    ):

        # 原始风险强度
        raw_risk = (
            dv_rate
            *
            (1 / (spectral_gap + 1e-6))
        )


        # 映射到 0-1
        risk_index = (
            raw_risk /
            (1 + raw_risk)
        )


        return risk_index