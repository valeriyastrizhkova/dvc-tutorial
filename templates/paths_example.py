"""Paths that work on every computer: the pattern from page 4, section 5.

Put this at the top of every script in scripts/. It finds the repository folder from the
script's own location, so it works on any laptop, in any editor, from any working folder.
"""
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]   # scripts/ is one level below the repository

with open(ROOT / "config.yaml", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# File names come from config.yaml, never from the code
spec = config["inputs"]["cpi"]
cpi = pd.read_excel(ROOT / spec["file"], sheet_name=spec["sheet"])

# Never: os.chdir(...), or paths like C:\Users\<name>\...
