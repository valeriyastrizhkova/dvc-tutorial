"""One script for every variation of the model: the variation lives in params.yaml.

    uv run dvc exp run -S model.lag=2
    uv run dvc exp run -S "model.squares=[debt_ratio]"
    uv run dvc exp run -S model.country_effects=true

Reads data/panel.csv, fits  score ~ drivers  by ordinary least squares, and writes:
  - outputs/coefficients.csv   the estimated coefficients
  - metrics/model.json         fit statistics, compared across experiments by dvc exp show
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

params = yaml.safe_load(open("params.yaml", encoding="utf-8"))
data_params, model = params["data"], params["model"]

panel = pd.read_csv("data/panel.csv").sort_values(["country", "year"])

# Drivers, lagged by model.lag years within each country
features = list(model["features"])
lagged = panel.groupby("country")[features].shift(model["lag"])
X = lagged.copy()
for name in model.get("squares", []):
    X[f"{name}_squared"] = lagged[name] ** 2

frame = pd.concat([panel[["country", "year", "score"]], X], axis=1).dropna()
frame = frame[frame["year"].between(data_params["start_year"], data_params["end_year"])]

columns = [c for c in frame.columns if c not in ("country", "year", "score")]
blocks = [np.ones(len(frame)), frame[columns].to_numpy()]
if model.get("country_effects", False):
    # One level per country (the first country is the reference)
    dummies = pd.get_dummies(frame["country"], drop_first=True, dtype=float)
    blocks.append(dummies.to_numpy())
design = np.column_stack(blocks)
target = frame["score"].to_numpy()
coef, *_ = np.linalg.lstsq(design, target, rcond=None)

residuals = target - design @ coef
n, k = design.shape
r2 = 1 - (residuals ** 2).sum() / ((target - target.mean()) ** 2).sum()

Path("outputs").mkdir(exist_ok=True)
terms = ["intercept", *columns]
pd.DataFrame({"term": terms, "coefficient": coef[:len(terms)].round(5)}).to_csv(
    "outputs/coefficients.csv", index=False, lineterminator="\n")

Path("metrics").mkdir(exist_ok=True)
metrics = {
    "observations": int(n),
    "r2": round(float(r2), 4),
    "adjusted_r2": round(float(1 - (1 - r2) * (n - 1) / (n - k)), 4),
    "rmse": round(float(np.sqrt((residuals ** 2).mean())), 3),
}
with open("metrics/model.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(metrics, f, indent=2)
print(metrics)
