# <Project name>

<One or two sentences: what the project produces, and for whom.>

## What it does

<The steps of the calculation, in plain words. For example:>

1. <Projects price growth by sector, region and scenario.>
2. <Gives countries without their own projection the prices of a proxy region.>

## Where the data comes from

| Input | Source | Updated |
|---|---|---|
| `data/raw/<file>` | <who provides it, or where it is downloaded> | <how often> |
| `data/reference/<file>` | <maintained by us: what it contains> | <when it changes> |

## How to run it

```powershell
uv sync
uv run dvc pull
uv run dvc repro
```

The results are in `outputs/`. Summary figures are in `metrics/`.

## Who to ask

<Name, team, and what they can answer.>
