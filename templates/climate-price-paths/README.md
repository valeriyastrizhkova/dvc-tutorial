# climate-price-paths: example files

The invented example from [page 5 of the tutorial](../../docs/5-worked-example.md). The two stage
scripts work: their calculation is a simple placeholder, to replace with your own.

| File | Copy it to | What it is |
|---|---|---|
| `config.yaml` | the repository root | Every file name and setting the scripts use |
| `dvc.yaml` | the repository root | The two-stage pipeline |
| `helpers.py` | `scripts\helpers.py` | Finds the repository folder and reads the config |
| `01_sector_prices.py` | `scripts\01_sector_prices.py` | Stage 1: price growth by sector |
| `02_add_countries.py` | `scripts\02_add_countries.py` | Stage 2: countries from proxy regions, plus a coverage metric |
| `.gitattributes` | the repository root | Keeps metrics files byte for byte on Windows, so a fresh clone matches `dvc.lock` |
| `publish_version.py` | `scripts\publish_version.py` | Delivers a version to a new S3 folder, and records it |

The scripts need `pandas`, `openpyxl`, `pyarrow` and `pyyaml`, and `boto3` for publishing:
`uv add pandas openpyxl pyarrow pyyaml boto3`.
