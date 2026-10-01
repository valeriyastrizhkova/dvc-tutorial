"""Shared helpers for the climate-price-paths scripts."""
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]   # the repository folder, on every computer


def load_config() -> dict:
    with open(ROOT / "config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def read_input(spec: dict) -> pd.DataFrame:
    """Read an Excel input described in config.yaml as {file: ..., sheet: ...}."""
    return pd.read_excel(ROOT / spec["file"], sheet_name=spec["sheet"])
