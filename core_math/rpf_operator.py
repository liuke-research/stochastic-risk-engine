import numpy as np


class RPFOperator:


    def spectral_gap(self, states):
        """
        Spectral analysis of market state dynamics.

        PCA eigenvalue separation is used as
        a proxy for dominant regime persistence.
        """


        cov = np.cov(
            states.T
        )


        eigvals = np.linalg.eigvals(
            cov
        )


        eigvals = np.sort(
            np.real(eigvals)
        )[::-1]


        # eigenvalue separation
        gap = (
            eigvals[0]
            -
            eigvals[1]
        )


        # normalized spectral persistence
        gap_ratio = (
            gap /
            (eigvals[0] + 1e-8)
        )


        return eigvals, gap_ratio