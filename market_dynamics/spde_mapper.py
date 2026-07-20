import numpy as np

class SPDEMapper:

    def simulate(self, n=1000):
        """
        toy stochastic system (SPDE proxy)
        """

        x = np.zeros(n)
        noise = np.random.normal(0, 1, n)

        for t in range(1, n):
            x[t] = x[t-1] + 0.1 * np.sin(x[t-1]) + 0.3 * noise[t]

        return x