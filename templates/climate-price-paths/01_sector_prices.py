"""Stage 1: project price growth by sector, region, scenario and year.

Reads consumer-price, power-price and gas-price scenarios and the sector weights,
all named in config.yaml. Each scenario sheet has the columns: scenario, region, year, value.
The weights sheet has the columns: sector, w_cpi, w_power, w_gas.

The calculation below is a simple placeholder: replace it with your own.
"""
from helpers import ROOT, load_config, read_input

config = load_config()
settings = config["sector_prices"]

cpi = read_input(config["inputs"]["cpi"]).rename(columns={"value": "cpi"})
power = read_input(config["inputs"]["power"]).rename(columns={"value": "power"})
gas = read_input(config["inputs"]["gas"]).rename(columns={"value": "gas"})
weights = read_input(config["inputs"]["weights"])

keys = ["scenario", "region", "year"]
drivers = cpi.merge(power, on=keys).merge(gas, on=keys)
drivers = drivers[drivers["year"] >= settings["base_year"]]

# Placeholder calculation: each sector's price growth is a weighted mix of the three drivers
prices = drivers.merge(weights, how="cross")
prices["price_growth"] = (prices["w_cpi"] * prices["cpi"]
                          + prices["w_power"] * prices["power"]
                          + prices["w_gas"] * prices["gas"])
prices = prices[["scenario", "region", "year", "sector", "price_growth"]]

output = ROOT / settings["output"]
output.parent.mkdir(exist_ok=True)
prices.to_parquet(output, index=False)
print(f"Wrote {output.relative_to(ROOT)}: {len(prices)} rows")
