import numpy as np

class DVLDPSolver:

    def rate_function(self, states):
        """
        proxy DV rate: empirical large deviation of volatility
        """

        vol = states[:, 1]

        mu = np.mean(vol)
        deviations = np.abs(vol - mu)

        I = np.mean(deviations ** 2)

        return I