import numpy as np

from data.hs300_loader import HS300Loader
from features.state_embedding import StateEmbedding

from core_math.harris_ergodicity import HarrisErgodicity
from core_math.rpf_operator import RPFOperator
from core_math.dv_ldp_solver import DVLDPSolver

from market_dynamics.regime_detector import RegimeDetector

from quant_signals.tail_risk_index import TailRiskIndex
from quant_signals.half_life import HalfLife
from analysis.rolling_engine import RollingRiskEngine

# ======================
# 1. Load HS300 market data
# ======================

loader = HS300Loader(
    "data/HS300.csv"
)

returns = loader.load()

print("\nMarket Dataset:")
print("HS300 Index")
print(f"Samples : {len(returns)}")


# ======================
# 2. State embedding
# ======================

embedder = StateEmbedding()

states = embedder.transform(
    returns,
    window=10
)

print(f"State dimension : {states.shape}")


# ======================
# 3. Harris mixing dynamics
# ======================

harris = HarrisErgodicity()

mixing_rate = harris.compute_mixing_rate(
    states
)


# 使用统一 half-life
hl = HalfLife().compute(
    mixing_rate
)


# ======================
# 4. RPF spectral analysis
# ======================

rpf = RPFOperator()

eigvals, gap = rpf.spectral_gap(
    states
)


# ======================
# 5. DV large deviation risk
# ======================

dv = DVLDPSolver()

dv_rate = dv.rate_function(
    states
)


# ======================
# 6. Regime detection
# ======================

regime = RegimeDetector().detect(
    mixing_rate,
    gap
)


# ======================
# 7. Tail Risk Index
# ======================

tri = TailRiskIndex().compute(
    dv_rate,
    gap
)


# ======================
# 8. Final Report
# ======================

print("\n======================================")
print("   HS300 STOCHASTIC RISK ENGINE")
print("======================================")

print(
    f"Mixing Rate (Harris) : {mixing_rate:.6f}"
)

print(
    f"Shock Half-life      : {hl:.2f} days"
)

print(
    f"Spectral Gap (RPF)   : {gap:.6f}"
)

print(
    f"DV Tail Risk Rate    : {dv_rate:.6f}"
)

print(
    f"Tail Risk Index      : {tri:.6f}"
)

print(
    f"Market Regime        : {regime}"
)

# ======================
# rolling risk analysis
# ======================

dates = loader.load_dates()


engine = RollingRiskEngine(
    window=250
)

print("START ROLLING ENGINE")
risk_df = engine.run(
    returns,
    dates,
    step=20
)
print("FINISH ROLLING ENGINE")

risk_df.to_csv(
    "HS300_risk_series.csv",
    index=False
)


print(
    "\nRolling risk saved:"
)

print(
    risk_df.tail()
)
print("======================================\n")