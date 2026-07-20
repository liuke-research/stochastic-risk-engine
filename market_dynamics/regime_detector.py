class RegimeDetector:

    def detect(self, mixing_rate, spectral_gap):
        """
        simple regime classification
        """

        if mixing_rate < 0.05:
            return "stable regime"
        elif spectral_gap < 0.1:
            return "transition regime"
        else:
            return "high instability regime"