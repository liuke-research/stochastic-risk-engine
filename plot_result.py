from visualization.risk_plot import RiskPlot


plotter = RiskPlot()


plotter.plot(
    price_file="data/HS300.csv",
    risk_file="HS300_risk_series.csv",
    save_path="HS300_risk.png"
)