"""Stage 2: give each country the prices of its proxy region.

Reads the stage 1 output and the country-to-region mapping named in config.yaml.
The mapping sheet has the columns: country, region.
Writes the final file for the other team, and a small coverage metric kept in git.
"""
import json

from helpers import ROOT, load_config, read_input

import pandas as pd

config = load_config()
settings = config["add_countries"]

prices = pd.read_parquet(ROOT / config["sector_prices"]["output"])
proxies = read_input(settings["proxies"])

# Every country gets the rows of the region it is mapped to
result = proxies.merge(prices, on="region", how="inner")
result = result[["scenario", "country", "region", "year", "sector", "price_growth"]]

output = ROOT / settings["output"]
output.parent.mkdir(exist_ok=True)
result.to_csv(output, index=False)
print(f"Wrote {output.relative_to(ROOT)}: {len(result)} rows")

# A small summary, kept in git so every pull request shows how it moved
missing = sorted(set(proxies["region"]) - set(prices["region"]))
(ROOT / "metrics").mkdir(exist_ok=True)
with open(ROOT / "metrics" / "coverage.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump({"countries": int(result["country"].nunique()),
               "regions_used": int(result["region"].nunique()),
               "proxy_regions_without_prices": missing}, f, indent=2)
