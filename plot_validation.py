import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from data.hs300_loader import HS300Loader


# =====================
# Risk series
# =====================

risk = pd.read_csv(
    "HS300_risk_series.csv"
)


# =====================
# Load processed returns
# =====================

loader = HS300Loader(
    "data/HS300.csv"
)

returns = loader.load()


returns = pd.DataFrame(
    {
        "return": returns
    }
)


returns["date"] = pd.read_csv(
    "data/HS300.csv"
)["date"]



# =====================
# Future volatility
# =====================

returns["future_vol"] = (
    returns["return"]
    .rolling(20)
    .std()
    .shift(-20)
)



# =====================
# Merge
# =====================

df = risk.merge(
    returns[["date","future_vol"]],
    on="date",
    how="inner"
)



print(df.head())



plt.figure(figsize=(6,5))


plt.scatter(
    df["tail_risk"],
    df["future_vol"],
    alpha=0.5
)


plt.xlabel(
    "Tail Risk Index"
)

plt.ylabel(
    "Future 20D Volatility"
)


plt.title(
    "Tail Risk vs Future Market Volatility"
)


plt.tight_layout()


plt.savefig(
    "risk_validation.png",
    dpi=300
)


plt.show()