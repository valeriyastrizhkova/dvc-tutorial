[Home](../README.md) › Going further › Experiments

# Track experiments with DVC

> **For you if** you try many variations of a model: other drivers, another lag, a squared term, a different sample, and you want to compare them without losing track.
>
> **You'll learn** to replace a copy of the script per idea with one script and its settings, run many variations at once, compare them in one table, and keep the winner.
>
> **Time:** about 45 minutes.
>
> **Before this page:** the [practice project](2-practice-project.md) up to step 8, so you know stages, params and metrics. Section 3 also works on its own, with its own example.

**On this page:**

- [1. The problem: one copy of the script per idea](#1-the-problem-one-copy-of-the-script-per-idea)
- [2. Try it on the practice project](#2-try-it-on-the-practice-project)
- [3. From many copied scripts to one](#3-from-many-copied-scripts-to-one)
- [4. Share and tidy up](#4-share-and-tidy-up)
- [5. Rules that keep experiments useful](#5-rules-that-keep-experiments-useful)

## 1. The problem: one copy of the script per idea

Research code often grows like this:

```
score_model.py
score_model_with_squares.py
score_model_lag2.py
score_model_full_sample.py
score_model_full_sample_v2.py
score_model_with_interest.py
results_basic.xlsx
results_squares.xlsx
results_lag2_FINAL.xlsx
...
```

Each new idea starts as a copy of the last script, with a few lines changed. After a few weeks there
are a dozen scripts that are 95% identical, and a dozen result files. Then the questions start:

- Which settings produced `results_lag2_FINAL.xlsx`, and on which version of the data?
- A bug is found in the shared part of the code. Which of the twelve copies have it?
- Which variation fitted best? Someone has to open twelve Excel files to find out.

**DVC experiments** fix this with one idea: **one script, and the variation lives in
`params.yaml`**. Each experiment is a run with different settings. DVC records the settings, the
data version and the results of every run, and compares them in one table.

## 2. Try it on the practice project

In your practice project (page 2), the `risk` stage reads `risk.confidence` and
`risk.window_days` from `params.yaml`. Let's try three time windows for the Value at Risk.

**Queue the experiments.** `--queue` saves each one to run later, and `-S` sets a parameter for
that experiment only:

```powershell
uv run dvc exp run --queue -n window-60  -S risk.window_days=60
uv run dvc exp run --queue -n window-120 -S risk.window_days=120
uv run dvc exp run --queue -n window-200 -S risk.window_days=200
```

`-n` gives each experiment a name. Without it, DVC invents one, such as `plain-tuba`.

**Run them all:**

```powershell
uv run dvc exp run --run-all
```

Each runs in its own temporary copy of the project, so **your files don't change**, and only the
stages affected by the setting rerun: here `risk`, but not `returns` or `climate_stress`.

**Compare them:**

```powershell
uv run dvc exp show --only-changed
```

You should see a table like this (shortened):

```
 Experiment    one_day_var_pct   annual_volatility_pct   risk.window_days
 workspace     2.177             16.219                  200
 main          2.177             16.219                  200
 ├── window-200  2.177           16.219                  200
 ├── window-120  2.331           18.145                  120
 └── window-60   2.823           22.082                  60
```

The shorter the window, the more it is dominated by the recent sell-off, so both the VaR and the
volatility rise. You found that in three commands, with every result kept next to its setting.

**Running one experiment directly** is also possible: `uv run dvc exp run -S risk.confidence=0.95`
runs it at once, in your own folder. It does change `params.yaml` and the outputs there, so undo
it afterwards with `git restore params.yaml metrics` and `uv run dvc checkout`. Queuing avoids that
step, which is why this page uses it.

## 3. From many copied scripts to one

The files for this section are in [`templates/experiments/`](../templates/experiments/). They use an
invented panel of 40 countries over 25 years, where a credit score (0 to 100) depends on growth,
debt, governance and interest costs.

### Set up the project

Copy `templates/experiments` to `C:\exp-practice`, then, in PowerShell:

```powershell
cd C:\exp-practice
git init -b main
uv init --bare
uv add pandas numpy pyyaml dvc
uv run python make_panel.py
uv run dvc init
Add-Content .gitattributes "**/metrics/** -text"   # keep metrics files byte for byte
uv run dvc add data/panel.csv
uv run dvc repro
git add .
git commit -m "Score model: baseline"
```

`make_panel.py` creates the invented data. `uv run dvc repro` fits the baseline model once.

### One script, every variation in `params.yaml`

`score_model.py` is the only model script. Everything that the copies used to change is a setting:

```yaml
data:
  start_year: 2000
  end_year: 2024

model:
  features: [gdp_growth, debt_ratio, governance]   # the drivers of the score
  lag: 1                                           # years between the drivers and the score
  squares: []                                      # drivers to add as squared terms
  country_effects: false                           # true: a separate level for each country
```

And `dvc.yaml` has a single stage that depends on those settings, and writes its fit statistics to
a metrics file:

```yaml
stages:
  fit:
    cmd: python score_model.py
    deps:
    - score_model.py
    - data/panel.csv
    params:
    - data
    - model
    outs:
    - outputs/coefficients.csv
    metrics:
    - metrics/model.json:
        cache: false
```

Compare that to the copies in section 1: each `score_model_….py` becomes one line of settings.

### Run a set of experiments

```powershell
uv run dvc exp run --queue -n squares -S "model.squares=[debt_ratio]"
uv run dvc exp run --queue -n country -S model.country_effects=true
uv run dvc exp run --queue -n country-squares -S model.country_effects=true -S "model.squares=[debt_ratio]"
uv run dvc exp run --queue -n country-squares-lag2 -S model.country_effects=true -S "model.squares=[debt_ratio]" -S model.lag=2
uv run dvc exp run --run-all
uv run dvc exp show --only-changed
```

You should see something like this (shortened):

```
 Experiment              observations   r2       rmse     model.lag   model.squares    model.country_effects
 main                    1000           0.4615   10.759   1           []               False
 ├── squares             1000           0.4626   10.749   1           ['debt_ratio']   False
 ├── country             1000           0.9763   2.258    1           []               True
 ├── country-squares     1000           0.9798   2.084    1           ['debt_ratio']   True
 └── country-squares-lag2 960           0.9409   3.571    2           ['debt_ratio']   True
```

Read it like a research log:

- **Country effects matter most.** Countries differ in their typical level, and the baseline model
  can't capture that: R² jumps from 0.46 to 0.98.
- **The squared debt term helps a little**, once country effects are in.
- **A two-year lag is worse**, and it loses 40 observations.

In this invented data the true answer is known, and `country-squares` finds it: its coefficients
are 1.22 for growth (true value 1.2) and 5.83 for governance (true value 6.0). To look at them,
bring the experiment into your folder and open its output:

```powershell
uv run dvc exp apply country-squares
Get-Content outputs\coefficients.csv
```

`dvc exp diff country country-squares` shows what changed between two experiments: their settings
and their metrics.

### Keep the winner

When you've chosen, turn the experiment into a branch, and bring it into `main` through a pull
request like any other change:

```powershell
git restore .
uv run dvc exp branch country-squares chosen-model
git switch chosen-model
uv run dvc checkout
```

`git restore .` first undoes the `exp apply` from above, so your folder is clean before you switch
branches.

The branch has `params.yaml` and `dvc.lock` exactly as the experiment left them. Push the branch,
open a pull request, and write in its description which experiments you compared and why you chose
this one. Once it's merged, `main` contains the chosen model, and the other experiments stay
available for comparison until you remove them.

## 4. Share and tidy up

- **Share experiments with a colleague:** `uv run dvc exp push origin <name>` sends an experiment
  to GitHub and to the DVC storage. Your colleague gets it with `uv run dvc exp pull origin <name>`,
  and sees it in their own `dvc exp show`.
- **See which experiments exist:** `uv run dvc exp list`.
- **Remove experiments you no longer need:** `uv run dvc exp remove <name>`, or
  `uv run dvc exp remove -A` to remove all of them.

## 5. Rules that keep experiments useful

1. **One script per model, never a copy per idea.** If an idea needs new code, add it behind a
   setting, as `country_effects` is in `score_model.py`.
2. **Every choice you vary is a setting in `params.yaml`**, and the script reads it.
3. **Results go to metrics files, not Excel files at the root.** `dvc exp show` can only compare
   what's in a metrics file.
4. **Name your experiments** with `-n`, so the table reads like a log.
5. **Write down what you concluded.** A short table in the README or in the pull request,
   "tried … because …, chose … because …", is worth more than the experiments themselves a year
   later.
6. **When two models are genuinely different**, for example a panel regression and a machine-learning
   model, give each its own stage. Put the code they share, such as data preparation, in one module
   that both import.

## In short

- **One script per model; every variation is a setting in `params.yaml`.**
- **`dvc exp run --queue` then `--run-all`** runs a set of variations without touching your files; **`dvc exp show`** compares them.
- **The winner becomes a branch with `dvc exp branch`**, and reaches `main` through a pull request.
- **Write down what you tried and why**: the conclusion matters more than the runs.

---

← [Previous: Good habits](6-good-habits.md) · [Next: Replace a home-made runner with DVC](replace-a-runner.md) →
