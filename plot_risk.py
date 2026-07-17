import pandas as pd
import matplotlib.pyplot as plt


# 读取rolling风险结果

df = pd.read_csv(
    "HS300_risk_series.csv"
)


print(df.head())


plt.figure(figsize=(12,4))


plt.plot(
    df["date"],
    df["tail_risk"]
)


plt.xlabel("Date")

plt.ylabel("Tail Risk Index")


plt.title(
    "HS300 Rolling Tail Risk Index"
)


plt.xticks(
    rotation=45
)


plt.tight_layout()


plt.savefig(
    "tail_risk_curve.png",
    dpi=300
)


plt.show()