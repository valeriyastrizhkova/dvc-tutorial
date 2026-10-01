"""Check that a hand-off file matches what the next part of the pipeline expects.

    uv run python check_handoff.py data/intermediate/macro_projection.csv

The expected columns of each hand-off file are listed in HANDOFFS below. Keep this list in step
with docs/handoffs.md. The check stops with an error, and a clear message, if a column is
missing, if a key column has empty values, or if the same key appears twice.
"""
import sys
from pathlib import Path

import pandas as pd

HANDOFFS = {
    "macro_projection.csv": {
        "columns": ["scenario", "country", "year", "gdp_growth", "debt_ratio"],
        "keys": ["scenario", "country", "year"],
    },
    "score_projection.csv": {
        "columns": ["scenario", "country", "year", "score"],
        "keys": ["scenario", "country", "year"],
    },
}


def check(path: Path) -> list[str]:
    spec = HANDOFFS.get(path.name)
    if spec is None:
        return [f"{path.name} is not listed in HANDOFFS"]
    frame = pd.read_csv(path)
    problems = [f"missing column: {c}" for c in spec["columns"] if c not in frame.columns]
    if problems:
        return problems
    keys = spec["keys"]
    empty = frame[keys].isna().any(axis=1).sum()
    if empty:
        problems.append(f"{empty} rows have an empty key ({', '.join(keys)})")
    duplicates = frame.duplicated(subset=keys).sum()
    if duplicates:
        problems.append(f"{duplicates} rows repeat the same key ({', '.join(keys)})")
    return problems


if __name__ == "__main__":
    failed = False
    for name in sys.argv[1:]:
        problems = check(Path(name))
        for problem in problems:
            print(f"{name}: {problem}")
        failed = failed or bool(problems)
    if not failed:
        print("Hand-off files look as expected.")
    sys.exit(1 if failed else 0)
