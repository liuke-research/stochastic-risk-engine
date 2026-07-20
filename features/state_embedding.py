import numpy as np


class StateEmbedding:
    """
    map returns -> high dimensional market state space

    Features:
    1. momentum
    2. volatility
    3. mean return
    4. skewness
    5. kurtosis
    6. drawdown
    7. return range
    """


    def transform(self, returns, window=20):

        states = []


        for i in range(window, len(returns)):

            window_data = returns[i-window:i]


            # 1 momentum
            momentum = np.sum(window_data)


            # 2 volatility
            volatility = np.std(window_data)


            # 3 mean return
            mean_return = np.mean(window_data)


            # 4 skewness
            std = np.std(window_data)

            if std > 0:
                skewness = (
                    np.mean(
                        (window_data - mean_return)**3
                    )
                    /
                    std**3
                )
            else:
                skewness = 0


            # 5 kurtosis
            if std > 0:
                kurtosis = (
                    np.mean(
                        (window_data - mean_return)**4
                    )
                    /
                    std**4
                )
            else:
                kurtosis = 0


            # 6 drawdown
            cumulative = np.cumsum(window_data)

            peak = np.maximum.accumulate(
                cumulative
            )

            drawdown = np.min(
                cumulative - peak
            )


            # 7 return range
            price_range = (
                np.max(window_data)
                -
                np.min(window_data)
            )


            states.append(
                [
                    momentum,
                    volatility,
                    mean_return,
                    skewness,
                    kurtosis,
                    drawdown,
                    price_range
                ]
            )


        states = np.array(states)


        # =========================
        # State normalization
        # =========================

        mean = np.mean(
            states,
            axis=0
        )

        std = np.std(
            states,
            axis=0
        )


        states = (
            states - mean
        ) / (
            std + 1e-8
        )


        return states