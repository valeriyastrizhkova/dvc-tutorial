[Home](../README.md) › Going further › Replace a home-made runner

# Replace a home-made runner with DVC

> **For you if** your project has a script that runs all the others in the right order, often called `run_all.py`, `run_pipeline.py` or `main.py`, and it has grown options, checks and logs over time.
>
> **You'll learn** which parts of a home-made runner DVC already does, how to migrate in five steps, and how to keep a familiar command if your team likes it.
>
> **Time:** about 45 minutes, plus the time to write your stages.
>
> **Before this page:** pages [1](1-how-dvc-works.md) and [2](2-practice-project.md), and ideally [page 5](5-worked-example.md), which turns scripts into stages step by step.

**On this page:**

- [1. Recognise it](#1-recognise-it)
- [2. What DVC replaces](#2-what-dvc-replaces)
- [3. Migrate in five steps](#3-migrate-in-five-steps)
- [4. Turn reports into metrics](#4-turn-reports-into-metrics)
- [5. Keep a thin runner, if the team likes it](#5-keep-a-thin-runner-if-the-team-likes-it)
- [6. Checklist](#6-checklist)

## 1. Recognise it

A home-made runner is often a well-made piece of work. This invented one runs a three-part
pipeline, macro projections, then credit scores, then loan pricing:

```python
STEPS = {
    "macro":   ["scripts/01_macro/01_prepare.py", "scripts/01_macro/02_project.py"],
    "scores":  ["scripts/02_Credit Scores/01_fit.py", "scripts/02_Credit Scores/02_project.py"],
    "pricing": ["scripts/03_Loan Pricing/01_fit.py", "scripts/03_Loan Pricing/02_project.py"],
}

# python run_all.py                 runs every part, in order
# python run_all.py --only scores   runs one part (its inputs must already exist)
# python run_all.py --check         checks that the input files exist
# Every run writes a log, and a manifest with a fingerprint (SHA-256) of each input file.
```

It has good ideas: one command to run everything, a check before running, and fingerprints of the
inputs. But look at what it can't do:

- **It reruns everything in a part, every time**, even if you only changed the last script.
- **Running one part alone needs its inputs "from an earlier run"**, and nothing tells you whether
  that earlier run is still up to date.
- **The fingerprints aren't linked to the code.** The manifest says which data was used, but not
  which version of the scripts.
- **A colleague who wants the results must rerun everything**, or get the files by hand.

DVC does all of the runner's work, and these four things as well. You keep your good ideas, and
lose the code you'd otherwise maintain.

## 2. What DVC replaces

| The runner | DVC |
|---|---|
| The list of steps, in order | `dvc.yaml`: each script is a stage, and the order follows from what each stage reads and writes |
| Run everything | `uv run dvc repro`, which only reruns what changed |
| `--only scores` | `uv run dvc repro scores_project`, which also brings anything it needs up to date first |
| `--check` (inputs exist) | `uv run dvc status` (what's out of date) and `uv run dvc repro --dry` (what would run) |
| `--list` | `uv run dvc dag` |
| A manifest with input fingerprints | `dvc.lock`: fingerprints of every input **and** output, committed with the code |
| A coverage or summary report | A metrics file, shown in every pull request and by `dvc metrics diff` |
| Download options | Download stages, pinned with a snapshot date ([page 3, section 3](3-your-own-project.md#3-write-the-pipeline)) |
| Upload of the results | A recorded delivery ([page 5, section 7](5-worked-example.md#7-deliver-a-version-with-a-record)) |
| The run log | Keep it: the wrapper in section 5 writes one for every run |

## 3. Migrate in five steps

Do this on a branch, for example `git switch -c dvc-pipeline`, and keep the old runner until the
new pipeline gives the same results.

### Step 1: remove spaces from folder names

Spaces in paths need quotes in every command and in `dvc.yaml`, and they're easy to get wrong.
Rename the folders with git, so their history follows them:

```powershell
git mv "scripts/02_Credit Scores" scripts/02_credit_scores
git mv "scripts/03_Loan Pricing" scripts/03_loan_pricing
```

Then update any paths in the code and the documentation that pointed to the old names.

### Step 2: write one stage per script

Go through `STEPS` in order. For each script, list what it **reads** (its `deps`) and what it
**writes** (its `outs`). Searching the script for `read_` and `to_` usually finds them:

```powershell
Select-String -Path scripts\02_credit_scores\01_fit.py -Pattern "read_|to_csv|to_excel|to_parquet"
```

For the credit-score part, that gives:

```yaml
stages:
  scores_fit:
    cmd: python scripts/02_credit_scores/01_fit.py
    deps:
    - scripts/02_credit_scores/01_fit.py
    - scripts/config.py
    - data/raw/score_history.xlsx
    - data/raw/governance.csv
    outs:
    - data/intermediate/score_coefficients.csv

  scores_project:
    cmd: python scripts/02_credit_scores/02_project.py
    deps:
    - scripts/02_credit_scores/02_project.py
    - scripts/config.py
    - data/intermediate/score_coefficients.csv
    - data/intermediate/macro_projection.csv     # written by macro_project
    outs:
    - outputs/credit_scores/score_projection.csv
    metrics:
    - metrics/score_coverage.json:
        cache: false
```

`data/intermediate/macro_projection.csv` is an output of the macro part and an input of this one.
That single line is how DVC knows that `scores_project` comes after `macro_project`, and why
`uv run dvc repro scores_project` brings the macro part up to date first if it needs to.

If a shared `config.py` holds paths and settings, list it in `deps`, as above. Better still, move
the settings that change into `params.yaml`, so each stage depends only on the ones it uses
([page 3, section 3](3-your-own-project.md#3-write-the-pipeline)).

### Step 3: stop changing folders inside scripts

DVC runs every command from the folder that contains `dvc.yaml`. If scripts call `os.chdir()` to
find their files, replace it with paths built from the repository folder
([page 4, section 5](4-existing-project.md#5-paths-that-work-on-every-computer)). Then each script
runs the same way from DVC, from PowerShell, and from your editor.

### Step 4: check that you get the same results

Run the new pipeline, then compare its outputs with those of the last run of the old runner:

```powershell
uv run dvc repro
```

Compare a few key numbers, or whole files, before deleting anything. Differences usually mean a
file that a script reads but that isn't in its `deps`, or a file it writes that isn't in its
`outs`.

### Step 5: put the data under DVC, and commit

```powershell
uv run dvc add data/raw
Add-Content .gitattributes "**/metrics/** -text"   # keep metrics files byte for byte
git status
git add .
git commit -m "Run the pipeline with DVC"
uv run dvc push
```

`git status` lists `dvc.yaml`, `dvc.lock`, `data/raw.dvc`, the metrics, and small `.gitignore` files
that DVC wrote next to each output folder. Check that no data file is in the list, then add them
all: DVC's `.gitignore` files already keep the data itself out of git. The `.gitattributes` line
keeps the metrics files byte for byte on Windows, as explained in
[DVC in your own project, section 2](3-your-own-project.md#2-add-dvc-to-an-existing-repository).

Now open a pull request. Once it's merged, everyone runs the same pipeline with the same command.

## 4. Turn reports into metrics

A coverage report ("how many countries got a result at each stage?") is valuable: keep it, but
write it as a small JSON file from the stage that knows the answer, and declare it in `metrics`:

```python
import json

coverage = {"countries": int(result["country"].nunique()),
            "missing": sorted(set(expected) - set(result["country"]))}
with open("metrics/score_coverage.json", "w", encoding="utf-8") as f:
    json.dump(coverage, f, indent=2)
```

Then `uv run dvc metrics show` prints every stage's coverage at once, and `uv run dvc metrics diff`
shows in a pull request whether a change lost or gained countries.

## 5. Keep a thin runner, if the team likes it

People get used to commands. If your team likes `run_pipeline.py --only scores`, keep that command,
but let it call DVC instead of the scripts.
[`templates/run_pipeline.py`](../templates/run_pipeline.py) is about 50 lines:

| Command | What it runs |
|---|---|
| `uv run python run_pipeline.py` | `dvc repro` |
| `uv run python run_pipeline.py --only scores` | `dvc repro scores_project` |
| `uv run python run_pipeline.py --check` | `dvc status`, then `dvc repro --dry` |
| `uv run python run_pipeline.py --list` | `dvc dag` |

It also writes a log of every run to `logs/`, the one thing a home-made runner usually does better
than DVC. Edit its `PARTS` so each part names the last stage of that part in your `dvc.yaml`, and
add `logs/` to `.gitignore`.

## 6. Checklist

- [ ] No folder or file name contains a space
- [ ] Every script is a stage, with everything it reads in `deps` and everything it writes in `outs`
- [ ] No `os.chdir()` in the scripts
- [ ] The new pipeline gives the same results as the old runner
- [ ] Raw data is under DVC, not in git
- [ ] Reports are metrics files, and `.gitattributes` contains `**/metrics/** -text`
- [ ] The old runner is deleted, or reduced to a thin wrapper around DVC

## In short

- **DVC already does a runner's work**: the order, running one part, checks, and fingerprints of inputs, now linked to the code.
- **Migrate in five steps**: names without spaces, one stage per script, no `os.chdir()`, check the results match, then commit.
- **Reports become metrics**, visible in every pull request.
- **A thin wrapper** can keep `--only`, `--check` and the run log, while DVC does the work.

---

← [Previous: Track experiments with DVC](experiments.md) · [Next: A pipeline owned by several people](several-owners.md) →
