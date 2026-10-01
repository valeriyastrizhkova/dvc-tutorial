"""Create an invented panel of countries and years to practise experiments on.

    uv run python make_panel.py

Writes data/panel.csv with: country, year, score (0-100, higher is better),
and four drivers: gdp_growth, debt_ratio, governance, interest_burden.
"""
from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
countries = [f"Country {i:02d}" for i in range(1, 41)]
years = range(1998, 2025)

rows = []
for country in countries:
    level = rng.normal(60, 12)
    governance = rng.normal(0, 1)
    debt = rng.uniform(20, 120)
    for year in years:
        growth = rng.normal(2.5, 2.0)
        debt = max(5.0, debt + rng.normal(1.0, 4.0) - 0.3 * growth)
        governance += rng.normal(0, 0.05)
        interest = max(0.2, 0.03 * debt + rng.normal(0, 0.4))
        rows.append((country, year, growth, debt, governance, interest, level))

panel = pd.DataFrame(rows, columns=["country", "year", "gdp_growth", "debt_ratio",
                                    "governance", "interest_burden", "level"])
# The score responds to last year's drivers, and to debt more strongly when debt is high
lagged = panel.groupby("country")[["gdp_growth", "debt_ratio", "governance", "interest_burden"]].shift(1)
panel["score"] = (panel["level"] + 1.2 * lagged["gdp_growth"] - 0.10 * lagged["debt_ratio"]
                  - 0.0015 * lagged["debt_ratio"] ** 2 + 6.0 * lagged["governance"]
                  - 1.5 * lagged["interest_burden"] + rng.normal(0, 2.0, len(panel)))
panel["score"] = panel["score"].clip(0, 100).round(2)
panel = panel.drop(columns="level").dropna()

Path("data").mkdir(exist_ok=True)
panel.round(4).to_csv("data/panel.csv", index=False, lineterminator="\n")
print(f"Wrote data/panel.csv: {panel['country'].nunique()} countries, {len(panel)} rows")
