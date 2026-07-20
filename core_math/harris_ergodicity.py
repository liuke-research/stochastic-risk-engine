import numpy as np



class HarrisErgodicity:


    def __init__(
        self,
        quantile=0.9,
        recovery_window=60,
        min_rate=1e-4
    ):

        # extreme deviation threshold
        self.quantile = quantile

        # recovery observation length
        self.recovery_window = recovery_window

        # numerical stability
        self.min_rate = min_rate



    def compute_mixing_rate(self, states):


        """
        Estimate exponential recovery rate:

        D(t)=D0 exp(-lambda t)

        where D(t) is deviation from
        stochastic equilibrium state.
        """



        # equilibrium center

        center = np.mean(
            states,
            axis=0
        )


        # distance from equilibrium

        deviation = np.linalg.norm(
            states - center,
            axis=1
        )



        # extreme shock threshold

        threshold = np.quantile(
            deviation,
            self.quantile
        )


        shock_points = np.where(
            deviation > threshold
        )[0]



        decay_rates = []



        for t in shock_points:


            if (
                t + self.recovery_window
                >= len(deviation)
            ):
                continue



            recovery_path = deviation[
                t:t+self.recovery_window
            ]


            d0 = recovery_path[0]


            if d0 <= 0:
                continue



            normalized = (
                recovery_path / d0
            )



            log_decay = np.log(
                normalized + 1e-10
            )



            time = np.arange(
                len(log_decay)
            )



            slope = np.polyfit(
                time,
                log_decay,
                1
            )[0]



            # only exponential recovery

            if slope < 0:

                rate = -slope


                if rate > 0:

                    decay_rates.append(
                        rate
                    )



        # no valid recovery

        if len(decay_rates) == 0:

            return self.min_rate



        # robust estimation

        mixing_rate = np.median(
            decay_rates
        )



        return max(
            mixing_rate,
            self.min_rate
        )



    def half_life(
        self,
        mixing_rate
    ):


        mixing_rate = max(
            mixing_rate,
            self.min_rate
        )


        return (
            np.log(2)
            /
            mixing_rate
        )