"""
explore_international_visitors.py
Loads parsed outputs and generates summary & visualizations.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)


def main():
    meta = pd.read_csv(OUT / "series_master.csv")
    obs = pd.read_csv(OUT / "observations_long.csv", parse_dates=["date"])
    df = obs.merge(meta, on="series_id")

    latest = df["date"].max()
    latest_vals = df[df["date"] == latest]
    top10 = latest_vals.sort_values("value", ascending=False).head(10)
    top10.to_csv(OUT / "top10_latest.csv", index=False)

    print(f"Top 10 series for {latest.date()} saved → outputs/top10_latest.csv")

    # Plot top 5
    top5 = top10["series_id"].head(5).tolist()
    pivot = df[df["series_id"].isin(top5)].pivot_table(
        index="date", columns="full_path", values="value", aggfunc="sum"
    )
    plt.figure(figsize=(10, 6))
    for col in pivot.columns:
        plt.plot(pivot.index, pivot[col], marker="o", label=col)
    plt.title("Top 5 Visitor Series Over Time")
    plt.xlabel("Date")
    plt.ylabel("Arrivals")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUT / "plot_top5_series.png")
    print("Plot saved → outputs/plot_top5_series.png")

    # Missing data summary
    miss = df.groupby("full_path")["value"].apply(lambda s: s.isna().mean())
    miss.to_csv(OUT / "missing_by_series.csv")
    print("Missingness summary saved → outputs/missing_by_series.csv")


if __name__ == "__main__":
    main()
