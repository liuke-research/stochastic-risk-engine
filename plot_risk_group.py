import pandas as pd
import matplotlib.pyplot as plt

from data.hs300_loader import HS300Loader


# =====================
# 1. Load risk series
# =====================

risk = pd.read_csv(
    "HS300_risk_series.csv"
)


risk["date"] = pd.to_datetime(
    risk["date"]
)



# =====================
# 2. Load processed returns
# =====================

loader = HS300Loader(
    "data/HS300.csv"
)


returns = loader.load()


# 构造DataFrame

returns = loader.load()

dates = loader.load_dates()


returns = pd.DataFrame(
    {
        "date": pd.to_datetime(dates),
        "return": returns
    }
)


# =====================
# 3. Future volatility
# =====================

returns["future_vol"] = (
    returns["return"]
    .rolling(20)
    .std()
    .shift(-20)
)



# =====================
# 4. Merge
# =====================

df = risk.merge(
    returns[["date", "future_vol"]],
    on="date",
    how="inner"
)


print(df.head())



# =====================
# 5. Risk groups
# =====================

df["risk_group"] = pd.qcut(
    df["tail_risk"],
    q=3,
    labels=[
        "Low Risk",
        "Medium Risk",
        "High Risk"
    ]
)



group = (
    df.groupby(
        "risk_group",
        observed=True
    )["future_vol"]
    .mean()
)



print("\nFuture volatility by risk regime:")
print(group)



# =====================
# 6. Plot
# =====================

plt.figure(
    figsize=(6,4)
)


group.plot(
    kind="bar"
)


plt.ylabel(
    "Average Future 20D Volatility"
)


plt.title(
    "Future Volatility across Tail Risk Regimes"
)


plt.xticks(
    rotation=0
)


plt.tight_layout()


plt.savefig(
    "risk_regime_validation.png",
    dpi=300
)


plt.show()