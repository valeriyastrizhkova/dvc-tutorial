[Home](../README.md) › Track 1: Clean up an existing project › Page 4

# 4. Bring an existing project into git and DVC

> **For you if** you're on track 1. Your project grew for months in a folder, with scripts, Excel inputs, results and notes, and was pushed to GitHub as it was.
>
> **You'll learn** to turn it into a repository anyone on the team can use, run and trust: a clean layout, paths that work everywhere, versioned data, and a branch workflow.
>
> **Time:** about 1 hour, plus the time to move your own files.
>
> **Before this page:** [page 1](1-how-dvc-works.md) and steps 1 to 5 of the [practice project](2-practice-project.md), where you use `dvc add`, `dvc push` and `dvc pull`.

**On this page:**

- [1. Take stock: recognise the signs](#1-take-stock-recognise-the-signs)
- [2. Decide where each file goes](#2-decide-where-each-file-goes)
- [3. Start with a clean `main`](#3-start-with-a-clean-main)
- [4. The new layout](#4-the-new-layout)
- [5. Paths that work on every computer](#5-paths-that-work-on-every-computer)
- [6. Stop keeping versions in file names](#6-stop-keeping-versions-in-file-names)
- [7. Excel files](#7-excel-files)
- [8. List your packages](#8-list-your-packages)
- [9. The `.gitignore`](#9-the-gitignore-and-gitattributes)
- [10. First commit, then put the data under DVC](#10-first-commit-then-put-the-data-under-dvc)
- [11. Work with branches from now on](#11-work-with-branches-from-now-on)
- [12. Check your repository](#12-check-your-repository)

We use an invented example, **climate-price-paths**: a research project that projects energy and
consumer prices under climate scenarios. Replace its names with yours as you go.

## 1. Take stock: recognise the signs

This is climate-price-paths before the clean-up. It was all pushed to a personal branch called
`all-my-work`, and `main` was left almost empty:

```
climate-price-paths/
├── price_model.py
├── price_model_V2.py              ← the first step of the calculation
├── price_model_V3.py              ← not a newer version: the second step
├── helpers - Copy.py
├── test.py                        ← empty, created by the editor
├── inputs/
│   ├── cpi_scenarios.xlsx
│   ├── power_prices.xlsx
│   ├── gas_prices.xlsx
│   ├── sector_weights.xlsx
│   ├── sector_weights_AM.xlsx     ← someone's personal copy
│   ├── emissions.zip
│   └── emissions (1)/emissions.csv  ← the same data again, unzipped
├── results_final.xlsx             ← 85 MB
├── results_final_v2.xlsx
├── charts/                        ← 60 PNG files
├── __pycache__/
└── notes.docx
```

And inside the scripts:

```python
os.chdir(r"C:\Users\A_MARTIN\Documents\GitHub\climate-price-paths")
weights = pd.read_excel(r"C:\Users\A_MARTIN\OneDrive\Projects\inputs\sector_weights.xlsx")
```

Look for the same signs in your own project:

| Sign | What goes wrong |
|---|---|
| All the work is on a personal branch, and `main` is empty | Colleagues looking at `main` see nothing, and there's no "official" version |
| Excel files and results are in git | The repository grows with every change, and never shrinks. GitHub warns above 50 MB per file, and refuses above 100 MB. |
| Versions in file names: `_V2`, `_final`, `- Copy`, `(1)`, initials | Nobody knows which file is current. That's exactly what git and DVC are for. |
| Paths like `C:\Users\<name>\...` and `os.chdir()` | The code only runs on one person's laptop |
| The code reads files that aren't in the repository | Results can't be reproduced from the repository |
| `__pycache__`, charts and reports in git | Noise in every commit, and conflicts when two people regenerate them |
| No list of packages | Nobody else can recreate the Python environment |
| Results delivered by hand, for example uploaded to S3 | No record of which version was delivered |

If you recognise several, this page is for you. None of them means the work is bad: they mean the
project outgrew its folder.

## 2. Decide where each file goes

Go through the project folder once, and put every file in one of four groups:

| Kind of file | Goes to | In climate-price-paths |
|---|---|---|
| Code you wrote | **git** | the `.py` scripts |
| Small text settings | **git** | a new `config.yaml` (see [section 5](#5-paths-that-work-on-every-computer)) |
| Data you received or downloaded | **DVC** | the Excel inputs, `emissions.csv` |
| Results your code produces | **DVC, as pipeline outputs** ([page 5](5-worked-example.md)) | `results_final.xlsx`, the charts |
| Large documents, such as PDFs and Word files | **DVC**, or your team's document store | `notes.docx` |
| Copies, old versions, empty test files | **Delete** (after checking they're really copies) | `helpers - Copy.py`, `test.py`, `emissions.zip`, `sector_weights_AM.xlsx` |
| Generated or personal files | **Ignored** by git | `__pycache__/`, editor settings |
| Passwords and keys | **Never in git**: in `.env` or your AWS profile | |

Two questions help with the hard cases:

- **"Can my code recreate this file?"** If yes, it's a result: don't keep it by hand, let the
  pipeline produce it.
- **"Is this the same data as another file?"** If yes, keep one and delete the other. Git and DVC
  keep the old versions for you from now on.

## 3. Start with a clean `main`

You might think you can just delete the big files from git now. You can, but **the repository won't
get smaller**: git keeps every file it ever stored in its history, so the old Excel versions stay
there for ever. Cleaning that history is possible, but it's an expert operation.

The simplest, safest way is to **start a new repository** with the clean layout, and keep the old
one as an archive:

1. On GitHub, create a new, empty repository, for example `climate-price-paths`. If you want to
   keep the old name, rename the old repository first, for example to `climate-price-paths-archive`
   (*Settings → General → Repository name*).
2. Clone the new repository into `C:\projects`, and build the new layout in it (sections 4 to 9).
3. Copy your files into the new layout, following the groups from section 2.
4. When the new repository works, archive the old one: *Settings → General → Archive this
   repository*. It becomes read-only, but nothing is lost.

> **Good at git?** You could instead clean the history with `git filter-repo` and force-push. It
> rewrites every commit, so only do it if nobody else has cloned the repository.

## 4. The new layout

```
climate-price-paths/
├── README.md              what the project does, and how to run it
├── pyproject.toml         the Python packages (section 8)
├── uv.lock
├── .gitignore             what git must ignore (section 9)
├── .gitattributes         keeps metrics files byte for byte (section 9)
├── config.yaml            file names and settings, read by the scripts
├── dvc.yaml               the pipeline (page 5)
├── dvc.lock
├── scripts/
│   ├── 01_sector_prices.py
│   ├── 02_add_countries.py
│   └── helpers.py
├── data/
│   ├── raw/               inputs you received: under DVC
│   └── reference/         mappings and weights you maintain: under DVC
├── outputs/               results: produced by the pipeline
├── metrics/               small summary results: in git
└── docs/                  notes and methodology
```

Create the folders in the new repository:

```powershell
cd C:\projects\climate-price-paths
mkdir scripts, data\raw, data\reference, outputs, metrics, docs
```

Then copy the files in: scripts into `scripts\`, received data into `data\raw\`, the mappings and
weights you edit yourself into `data\reference\`. Leave `outputs\` empty: the pipeline fills it.

**Write the README now**, while you still remember everything. A template is in
[`templates/README-template.md`](../templates/README-template.md). It asks four questions: what
the project does, where the data comes from, how to run it, and who to ask. If you already wrote
a README describing your inputs and steps, keep it: it's the most valuable file in the project.

**Keep the README in step with the files.** Whenever you move or rename a file or a folder, update
every README that mentions it in the same commit. A README that points to folders that no longer
exist is worse than none: people trust it.

## 5. Paths that work on every computer

This is the change that lets anyone else run your code. Replace this:

```python
import os
import pandas as pd

os.chdir(r"C:\Users\A_MARTIN\Documents\GitHub\climate-price-paths")
cpi = pd.read_excel(r"C:\Users\A_MARTIN\Documents\GitHub\climate-price-paths\inputs\cpi_scenarios.xlsx",
                    sheet_name="CPI")
```

with this:

```python
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]           # the repository folder, wherever it is
config = yaml.safe_load(open(ROOT / "config.yaml"))

cpi = pd.read_excel(ROOT / config["inputs"]["cpi"]["file"],
                    sheet_name=config["inputs"]["cpi"]["sheet"])
```

and keep the file names in `config.yaml`:

```yaml
inputs:
  cpi:
    file: data/raw/cpi_scenarios.xlsx
    sheet: CPI
  power:
    file: data/raw/power_prices.xlsx
    sheet: Prices
```

Three rules:

1. **Never use `os.chdir()`.** `ROOT` already points at the repository folder, on every computer.
2. **No `C:\Users\...` anywhere in the code.** Every path starts from `ROOT`.
3. **File names live in `config.yaml`, not in the code.** When an input changes, you edit one line,
   and DVC sees exactly which setting changed.

`Path(__file__).resolve().parents[1]` means "the folder above the one this script is in". Scripts
are in `scripts\`, so that's the repository folder. A full example is in
[`templates/paths_example.py`](../templates/paths_example.py).

## 6. Stop keeping versions in file names

From now on, **git and DVC keep the versions**, so each file has one name, for ever:

| Before | After | Why |
|---|---|---|
| `price_model.py`, `price_model_V2.py` | `scripts/01_sector_prices.py` | The old versions are in git's history |
| `price_model_V3.py` | `scripts/02_add_countries.py` | It was a different step, so its name says what it does |
| `helpers - Copy.py` | deleted | It was identical to `helpers.py` |
| `results_final.xlsx`, `results_final_v2.xlsx` | `outputs/prices_by_sector.xlsx` | Produced by the pipeline; DVC keeps every version |
| `sector_weights.xlsx`, `sector_weights_AM.xlsx` | `data/reference/sector_weights.xlsx` | One file. Changes go through a branch and a pull request (section 11). |
| `prices_20260831_1530_V2.xlsx` | `outputs/prices.xlsx` | The date and time of a version belong in git's history and `dvc.lock`, not in its name |
| Result files at the top of the repository, next to the README | `outputs/` | The top folder is for the files that describe and run the project |
| The same file in `data/` and in `scripts/` | one copy, in `data/` | Two copies always end up different |
| `02_Loan Pricing/` | `02_loan_pricing/` | Spaces in names need quotes in every command, and break easily |

Number pipeline scripts in the order they run (`01_`, `02_`), and name them after what they do.
Use lower case, digits and `_` or `-` in file and folder names, never spaces. To rename something
already in git, use `git mv`, so its history follows it: `git mv "02_Loan Pricing" 02_loan_pricing`.
To see an old version, use `git log` for code and the tag of a release for data, never a copy.

## 7. Excel files

Excel files are fine as inputs, but know two things:

- **Git can't show what changed in an Excel file.** It's a binary file, so git only sees "the file
  changed". That's why Excel files belong to DVC, not git: DVC versions them properly, without
  making the repository grow.
- **Excel leaves temporary files** like `~$sector_weights.xlsx` while a file is open, and it locks
  the file. Close Excel before running the pipeline, and ignore those files in git (section 9).

For inputs that change often, consider saving them as CSV or Parquet instead: other tools can
compare them, and they load faster.

## 8. List your packages

Record the Python version and every package the code imports, so that anyone gets the same
environment with one command:

```powershell
uv init --bare
uv python pin 3.12
uv add pandas openpyxl pyyaml statsmodels matplotlib
uv add "dvc[s3]"
```

Use the Python version you actually work with, and add every package your scripts import. Run
each script once with `uv run python scripts\<script>.py`: if one fails with
`ModuleNotFoundError`, add that package with `uv add` and try again.

A colleague then only needs `uv sync`.

**List every package the project uses, not just some.** A `requirements.txt` that lists only what
one helper script needs, for example the S3 upload, leaves everyone guessing the rest.
`pyproject.toml` should cover the whole project.

## 9. The `.gitignore` and `.gitattributes`

Copy [`templates/gitignore.txt`](../templates/gitignore.txt) into the repository as `.gitignore`.
It ignores the files that should never be in git: the environment, credentials, Python caches,
the temporary files Excel and Word leave while a file is open, and editor settings:

```
.venv/
.env

# Generated by Python
__pycache__/
*.pyc

# Temporary lock files left by Excel and Word while a file is open
~$*.xlsx
~$*.xls
~$*.docx

# Editor files
.spyproject/
.ipynb_checkpoints/
```

Data and outputs are not listed here on purpose: DVC adds its own entries for every file it tracks.

**Check that it works**, especially for credentials:

```powershell
git check-ignore -v .env
```

It prints the `.gitignore` line that ignores `.env`. **If it prints nothing, `.env` is not
ignored**, and your keys could end up on GitHub with the next `git add .`. A sentence in a README
saying ".env must never be committed, see .gitignore" protects nothing if the `.gitignore` doesn't
exist.

**Add one line to `.gitattributes` too**, for the metrics files you'll create on
[page 5](5-worked-example.md):

```powershell
Add-Content .gitattributes "**/metrics/** -text"   # keep metrics files byte for byte
```

It matters on Windows. Metrics files are kept in git, and `dvc.lock` records their hash. Without
this line, git changes their line endings when a colleague clones the repository, so the files no
longer match `dvc.lock`, and `dvc status` reports changes that aren't real. The line is also in
[`templates/gitattributes.txt`](../templates/gitattributes.txt).

## 10. First commit, then put the data under DVC

Commit the code, settings and README:

```powershell
git add README.md pyproject.toml uv.lock .python-version .gitignore .gitattributes config.yaml scripts docs
git status
git commit -m "Clean layout: scripts, config, README and packages"
```

Check with `git status` that no data file is in the list before committing.

**Read `git status` before every commit, not just this one.** It catches accidents no rule can
catch. For example, while it saves a workbook, Excel writes a temporary copy with no extension and
an eight-character name, such as `A3F09C12`. If one is in the list, don't add it: delete it.

Then hand the data to DVC, and connect it to shared storage, as in
[page 3, section 2](3-your-own-project.md#2-add-dvc-to-an-existing-repository):

```powershell
uv run dvc init
uv run dvc add data/raw data/reference
uv run dvc remote add -d storage s3://your-company-bucket/climate-price-paths
git add .dvc .dvcignore data/raw.dvc data/reference.dvc data/.gitignore
git commit -m "Version input data with DVC"
uv run dvc push
git push
```

`dvc add data/raw` tracks the whole folder as one unit: when any file in it changes, run
`uv run dvc add data/raw` again to record a new version.

Your inputs are now versioned, and the repository stays small. [Page 5](5-worked-example.md) turns
the scripts into a pipeline, so the results are versioned too.

## 11. Work with branches from now on

The last habit makes everything else stick: **`main` is the truth, and every change reaches it
through a pull request.**

1. **Start each piece of work on a short branch**, named after what it does:

   ```powershell
   git switch main
   git pull
   git switch -c add-country-proxies
   ```

2. **Commit at the end of every working session**, with a message that says what changed and why:

   ```powershell
   git add scripts\02_add_countries.py config.yaml
   git commit -m "Assign regional prices to countries without their own projection"
   git push -u origin add-country-proxies
   ```

   "Update code" or "changes" tell nobody anything. A good message completes the sentence
   "This commit will…".

3. **Open a pull request on GitHub** when the work is ready, or earlier if you want feedback. GitHub
   shows a **Compare & pull request** button after you push. Ask a colleague to review it.

4. **Merge, then delete the branch.** GitHub offers both buttons on the pull request. Back on your
   laptop:

   ```powershell
   git switch main
   git pull
   ```

What to avoid:

- **One personal branch for everything.** It hides your work, and it can never be merged cleanly.
- **Long-lived branches.** A branch that lives for months drifts away from `main`. Days to a couple
  of weeks is a good size.
- **Feature branches that hold only a document.** If the work is done elsewhere, the branch name
  promises something that isn't there.

**Experiments and production code.** Research means trying many ideas, and only some become the
official model. Keep the two apart:

- **Try variations as DVC experiments**, not as copies of the script or long-lived branches
  ([Track experiments with DVC](experiments.md)).
- **The official version of every script lives only on `main`.** If an experiment wins, its change
  comes to `main` through a pull request, and the experiment branch is deleted.
- **Never keep a second copy of production code** in an experiment folder or a personal branch:
  the two copies drift apart, and nobody knows which one produced a result.

## 12. Check your repository

When you've finished, go through this list. Every "no" is a next step.

- [ ] `main` contains the current work, and has a README
- [ ] No file in git is bigger than a few hundred kilobytes
- [ ] No file name contains `_V2`, `_final`, `- Copy`, `(1)`, a date or someone's initials
- [ ] No file or folder name contains a space
- [ ] No result files at the top of the repository: results are in `outputs/`
- [ ] Each file exists in one place only, and production code exists only on `main`
- [ ] No `C:\Users\...` and no `os.chdir()` in the code
- [ ] File names and settings are in `config.yaml`
- [ ] `uv sync` on a fresh clone installs everything the scripts need
- [ ] All inputs are under DVC, and `uv run dvc pull` on a fresh clone gets them
- [ ] `.gitignore` covers `.venv`, `.env`, `__pycache__` and Excel lock files, and
      `git check-ignore -v .env` prints a rule
- [ ] `.gitattributes` contains `**/metrics/** -text`
- [ ] Every README matches the current files and folders
- [ ] Ongoing work is on short, named branches, merged through pull requests

The last test is the real one: **ask a colleague to clone the repository and run it**, without your
help. If they can, the project is ready.

## In short

- **Decide where each file goes:** git for code and settings, DVC for data and results, nowhere for copies, and never git for credentials.
- **Start a clean `main` in a new repository**, because deleting big files doesn't shrink git's history.
- **Paths start from the repository folder, file names live in `config.yaml`, and each file keeps one name for ever.**
- **Data goes under DVC, work happens on short branches, and the checklist tells you what's left.**

---

← [Previous: Practice project, step 5](2-practice-project.md#step-5--a-new-data-version-and-travelling-back-in-time) · [Next: Worked example](5-worked-example.md) →
