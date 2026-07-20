class HalfLife:

    def compute(self, mixing_rate):
        return 0.693 / (mixing_rate + 1e-8)