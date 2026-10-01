# Experiments: example files

The example from [Track experiments with DVC](../../docs/experiments.md), section 3. It works as it
is: copy this folder to `C:\exp-practice` and follow the page.

| File | What it is |
|---|---|
| `make_panel.py` | Creates an invented panel: 40 countries, 1998 to 2024, a score and four drivers |
| `score_model.py` | The only model script. Every variation comes from `params.yaml`. |
| `params.yaml` | The settings each experiment changes: drivers, lag, squared terms, country effects, sample |
| `.gitattributes` | Keeps `metrics/model.json` byte for byte on Windows, so a fresh clone matches `dvc.lock` |
| `dvc.yaml` | One stage, `fit`, that depends on those settings and writes `metrics/model.json` |
