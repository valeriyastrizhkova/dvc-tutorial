[Home](../README.md) › Both tracks › Page 2

# 2. Practice project

> **For you if** you've read [page 1](1-how-dvc-works.md), on either track. You'll do everything on a small, invented project on your laptop, so nothing can break.
>
> **You'll learn** to version data, go back in time, share data with a colleague, and (track 2) build a pipeline with settings and metrics.
>
> **Time:** about 30 minutes for steps 1 to 5 (track 1), about 1 hour for everything (track 2).
>
> **Before this page:** [page 1](1-how-dvc-works.md) and [Setup](setup.md).

**How to use this page:**

> **Track 1, clean up an existing project:** do steps 1 to 5. They teach how DVC versions data,
> which is what you need first. A box after step 5 sends you on to page 4.
>
> **Good at git?** Steps 1, 2 and 5 are routine for you: skim them.
>
> **Used DVC before?** Skim everything, but do [Step 8](#step-8--change-a-setting-and-watch-what-reruns)
> and the [exercises](#exercises): they show behaviour people often get wrong.
>
> **New to git?** Do every step, in order. Type the commands yourself rather than copying them.

**On this page:**

- [Step 1 – Copy the practice project and install DVC](#step-1--copy-the-practice-project-and-install-dvc)
- [Step 2 – Start git and DVC](#step-2--start-git-and-dvc)
- [Step 3 – Put the first version of the data under DVC](#step-3--put-the-first-version-of-the-data-under-dvc)
- [Step 4 – Set up shared storage and push](#step-4--set-up-shared-storage-and-push)
- [Step 5 – A new data version, and travelling back in time](#step-5--a-new-data-version-and-travelling-back-in-time)
- [Step 6 – Your first pipeline stage](#step-6--your-first-pipeline-stage)
- [Step 7 – A pipeline with settings and metrics](#step-7--a-pipeline-with-settings-and-metrics)
- [Step 8 – Change a setting and watch what reruns](#step-8--change-a-setting-and-watch-what-reruns)
- [Step 9 – Try an idea on a branch](#step-9--try-an-idea-on-a-branch)
- [Step 10 – Be your own colleague](#step-10--be-your-own-colleague)
- [Exercises](#exercises)

We will build a small version of what a real risk pipeline does: take market prices, compute a
portfolio's risk, and run a carbon-price stress test on company profits. Everything runs on your
laptop with made-up data, so you can't break anything.

## Step 1 – Copy the practice project and install DVC

Copy the [`practice-project`](../practice-project/) folder of this repository to `C:\dvc-practice`,
outside the company repositories and outside OneDrive. In PowerShell:

```powershell
git clone https://github.com/valeriyastrizhkova/dvc-tutorial.git C:\projects\dvc-tutorial   # get this tutorial
Copy-Item -Recurse C:\projects\dvc-tutorial\practice-project C:\dvc-practice                # copy the practice folder
```

If you already have this repository on your laptop, skip the `git clone` line and change the
path in the `Copy-Item` line to where it is. Run `Copy-Item` only once: if `C:\dvc-practice`
already exists, it puts a second copy inside it.

**In VS Code:** open `C:\dvc-practice` with *File → Open Folder*, then *Terminal → New Terminal*,
and skip the `cd` line below. After `uv sync`, select the `.venv` interpreter as in
[Setup, step 7](setup.md#step-7--optional-use-vs-code).

Then install DVC, in PowerShell:

```powershell
cd C:\dvc-practice
uv sync                # creates .venv and installs DVC, pandas, numpy, pyyaml
uv run dvc --version   # should print 3.x
```

You should see:

```text
Using CPython 3.14.4
Creating virtual environment at: .venv
Resolved 112 packages in 1ms
Installed 101 packages in 1.76s
 + aiohappyeyeballs==2.7.1
 + aiohttp==3.14.3
 ...                                   (about 100 lines, one per package)
 + zc-lockfile==4.0
3.67.1
```

Your Python version and the timings can be different. The first time, uv also downloads the
packages, so it can take a minute.

`uv sync` reads the package list in `pyproject.toml` and installs the exact versions written in
`uv.lock`, so everyone doing the tutorial gets the same packages.

From now on, every `dvc` and `python` command starts with `uv run`. It runs the command inside
`.venv`, so there is nothing to activate, and it works the same in every new terminal.

## Step 2 – Start git and DVC

```powershell
git init             # start a git history in this folder
uv run dvc init      # add DVC to it (creates the .dvc folder)
git add .
git commit -m "Start practice project with DVC"
git branch -M main   # name the main line of work "main"
```

You should see:

```text
Initialized empty Git repository in C:/dvc-practice/.git/
Initialized DVC repository.

You can now commit the changes to git.

+---------------------------------------------------------------------+
|                                                                     |
|        DVC has enabled anonymous aggregate usage analytics.         |
|     Read the analytics documentation (and how to opt-out) here:     |
|             <https://dvc.org/doc/user-guide/analytics>              |
|                                                                     |
+---------------------------------------------------------------------+

What's next?
------------
- Check out the documentation: <https://dvc.org/doc>
- Get help and share ideas: <https://dvc.org/chat>
- Star us on GitHub: <https://github.com/treeverse/dvc>
warning: in the working copy of '.gitattributes', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'pyproject.toml', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'uv.lock', LF will be replaced by CRLF the next time Git touches it
[master (root-commit) 41a2484] Start practice project with DVC
 12 files changed, 3287 insertions(+)
 create mode 100644 .dvc/.gitignore
 create mode 100644 .dvc/config
 create mode 100644 .dvcignore
 create mode 100644 .gitattributes
 create mode 100644 README.md
 create mode 100644 climate_stress.py
 create mode 100644 make_data.py
 create mode 100644 params.yaml
 create mode 100644 pyproject.toml
 create mode 100644 returns.py
 create mode 100644 risk.py
 create mode 100644 uv.lock
```

Two things in this output are normal:

- **The `warning: ... LF will be replaced by CRLF` lines.** Git on Windows is telling you how it
  stores line endings. You can ignore them, here and in later steps.
- **The commit id**, `41a2484` here. Yours is different, because it depends on your name and the
  time. The same goes for every commit id on this page.

You don't need to tell git to ignore `.venv`: `uv sync` already put a `.gitignore` inside it.

`dvc init` created a hidden `.dvc` folder. It holds DVC's settings (`.dvc/config`) and, later,
the cache.

## Step 3 – Put the first version of the data under DVC

Create the input data. In real life this would be a download from a data provider.

```powershell
uv run make_data.py
```

You should see:

```text
Wrote data/prices.csv (250 trading days) and data/companies.csv
```

This writes `data/prices.csv` (250 trading days for five companies) and `data/companies.csv`
(their emissions and profits). Now hand them to DVC:

```powershell
uv run dvc add data/prices.csv data/companies.csv
```

You should see:

```text
To track the changes with git, run:

	git add 'data\.gitignore' 'data\prices.csv.dvc' 'data\companies.csv.dvc'

To enable auto staging, run:

	dvc config core.autostage true
```

DVC ends many commands with this kind of hint. You don't need to follow it: this page always
gives you the `git add` to run next. From here on, the outputs below leave the hint out.

DVC did three things:

1. It computed the hash of each file and copied the files into `.dvc/cache`.
2. It created a small "pointer" file next to each one: `data/prices.csv.dvc` and `data/companies.csv.dvc`.
3. It added the real data files to `data/.gitignore`, so git will never try to store them.

Open `data/prices.csv.dvc` in any text editor. It looks like this:

```yaml
outs:
- md5: 6645fac464949232a02816779c89ca59
  size: 13262
  hash: md5
  path: prices.csv
```

That hash *is* this version of the data, and you should see exactly the same one: the practice
scripts write identical files on every computer. Save the pointers in git:

```powershell
git add data/prices.csv.dvc data/companies.csv.dvc data/.gitignore
git commit -m "Add input data, version 1"
```

You should see:

```text
[main efe1ca4] Add input data, version 1
 3 files changed, 12 insertions(+)
 create mode 100644 data/.gitignore
 create mode 100644 data/companies.csv.dvc
 create mode 100644 data/prices.csv.dvc
```

> **The key idea:** git now stores a 5-line pointer, not the data. The data itself stays in the
> DVC cache, and later in the remote.

## Step 4 – Set up shared storage and push

In a real project the remote is usually cloud storage, such as an S3 bucket. For practice we use a plain folder next to the
project, so no credentials are needed:

```powershell
uv run dvc remote add -d practice ../dvc-practice-storage   # -d makes it the default remote
git add .dvc/config
git commit -m "Configure practice storage"
uv run dvc push                                             # copies the cache to the remote
```

You should see:

```text
Setting 'practice' as a default remote.
[main 2da773d] Configure practice storage
 1 file changed, 4 insertions(+)
2 files pushed
```

Look inside `../dvc-practice-storage`: you'll see folders with hash-like names. That's where DVC
keeps every version. In a real project, the same line in `.dvc/config` points to cloud storage, for
example `url = s3://your-company-bucket/dvc-store`. [DVC in your own project](3-your-own-project.md) shows how to set that up.

## Step 5 – A new data version, and travelling back in time

The data provider sends a refresh with 20 more trading days, including a market sell-off:

```powershell
uv run make_data.py --update
uv run dvc status
```

You should see:

```text
Wrote data/prices.csv (270 trading days) and data/companies.csv
data\prices.csv.dvc:
	changed outs:
		modified:           data\prices.csv
```

`dvc status` tells you that `data/prices.csv` has changed. `data/companies.csv` hasn't: the script
rewrote it with the same content, and DVC compares content, not dates. Record the new version:

```powershell
uv run dvc add data/prices.csv
git add data/prices.csv.dvc
git commit -m "Refresh prices: 20 more trading days"
uv run dvc push
git log --oneline
```

You should see:

```text
[main a5c9f4e] Refresh prices: 20 more trading days
 1 file changed, 2 insertions(+), 2 deletions(-)
1 file pushed
a5c9f4e Refresh prices: 20 more trading days
2da773d Configure practice storage
efe1ca4 Add input data, version 1
41a2484 Start practice project with DVC
```

Only one file is pushed, the new prices: `companies.csv` and the old prices are already on the
remote.

Now go back to version 1 of the prices, without touching anything else:

```powershell
git checkout HEAD~1 -- data/prices.csv.dvc   # the pointer from one commit ago
uv run dvc checkout data/prices.csv.dvc      # make the data match the pointer
uv run python -c "import pandas as pd; print(len(pd.read_csv('data/prices.csv')), 'days')"
```

You should see:

```text
M       data\prices.csv
250 days
```

`M` means DVC modified the file in your folder. Come back to the latest version:

```powershell
git checkout HEAD -- data/prices.csv.dvc
uv run dvc checkout data/prices.csv.dvc
uv run python -c "import pandas as pd; print(len(pd.read_csv('data/prices.csv')), 'days')"
```

You should see:

```text
M       data\prices.csv
270 days
```

> **Remember the pair:** `git checkout` moves the pointers, `dvc checkout` moves the data to match.
> Every time you switch commits or branches, run `dvc checkout` afterwards.

> **Track 1, clean up an existing project:** you've learned what you need here. Go on to
> **[page 4: Bring an existing project into git and DVC →](4-existing-project.md)**
>
> **Track 2, build DVC pipelines:** carry on with step 6.

## Step 6 – Your first pipeline stage

So far DVC only stores data. Now let it run calculations too. The first stage turns prices into
daily returns:

```powershell
uv run dvc stage add -n returns `
  -d returns.py -d data/prices.csv `
  -o data/returns.csv `
  python returns.py
```

You should see:

```text
Added stage 'returns' in 'dvc.yaml'
```

In PowerShell, a backtick `` ` `` at the very end of a line means "the command continues on the
next line". You can also type it all on one line without the backticks.

Each option means:

| Option | Meaning |
|---|---|
| `-n returns` | the stage's name |
| `-d returns.py -d data/prices.csv` | its dependencies: if either changes, the stage reruns |
| `-o data/returns.csv` | its output: DVC stores and versions it |
| `python returns.py` | the command to run |

This wrote a file called `dvc.yaml`, the recipe. Run it:

```powershell
uv run dvc repro
```

You should see:

```text
'data\prices.csv.dvc' didn't change, skipping
Running stage 'returns':
> python returns.py
Wrote data/returns.csv (269 days)
Generating lock file 'dvc.lock'
Updating lock file 'dvc.lock'
Use `dvc push` to send your updates to remote storage.
```

DVC runs the stage and writes `dvc.lock`, the receipt. Open both files and compare: `dvc.yaml`
says *what should happen*, `dvc.lock` records *what did happen*, with hashes.

```powershell
git add dvc.yaml dvc.lock data/.gitignore
git commit -m "Add returns stage"
```

You should see:

```text
[main 6b04145] Add returns stage
 3 files changed, 27 insertions(+)
 create mode 100644 dvc.lock
 create mode 100644 dvc.yaml
```

## Step 7 – A pipeline with settings and metrics

Add the two other stages. They read their settings from `params.yaml`, and each writes a small
metrics file:

```powershell
uv run dvc stage add -n risk `
  -d risk.py -d data/returns.csv `
  -p risk `
  -o data/portfolio_returns.csv `
  -M metrics/risk.json `
  python risk.py

uv run dvc stage add -n climate_stress `
  -d climate_stress.py -d data/companies.csv `
  -p scenario `
  -o data/stressed.csv `
  -M metrics/stress.json `
  python climate_stress.py
```

You should see:

```text
Added stage 'risk' in 'dvc.yaml'
Added stage 'climate_stress' in 'dvc.yaml'
```

Two new options:

| Option | Meaning |
|---|---|
| `-p risk` | depends on the `risk` section of `params.yaml` only, not the whole file |
| `-M metrics/risk.json` | a metrics file that is **kept in git**, not in the cache, so every change is visible in a pull request |

Your `dvc.yaml` now looks like this. Real projects use exactly the same shape, just with more stages:

```yaml
stages:
  returns:
    cmd: python returns.py
    deps:
    - data/prices.csv
    - returns.py
    outs:
    - data/returns.csv
  risk:
    cmd: python risk.py
    deps:
    - data/returns.csv
    - risk.py
    params:
    - risk
    outs:
    - data/portfolio_returns.csv
    metrics:
    - metrics/risk.json:
        cache: false
  climate_stress:
    cmd: python climate_stress.py
    deps:
    - climate_stress.py
    - data/companies.csv
    params:
    - scenario
    outs:
    - data/stressed.csv
    metrics:
    - metrics/stress.json:
        cache: false
```

Run it and look at the results:

```powershell
uv run dvc repro          # returns is skipped (nothing changed); risk and climate_stress run
uv run dvc dag            # draws the pipeline in the terminal
uv run dvc metrics show   # prints both metrics files as a table
```

You should see:

```text
'data\prices.csv.dvc' didn't change, skipping
Stage 'returns' didn't change, skipping
Running stage 'risk':
> python risk.py
1-day VaR at 99%: 2.177% of portfolio value
Updating lock file 'dvc.lock'

'data\companies.csv.dvc' didn't change, skipping
Running stage 'climate_stress':
> python climate_stress.py
Orderly transition 2030: worst hit Echo Airlines (40.3% of profit)
Updating lock file 'dvc.lock'
Use `dvc push` to send your updates to remote storage.
+---------------------+
| data\prices.csv.dvc |
+---------------------+
            *
            *
            *
      +---------+
      | returns |
      +---------+
            *
            *
            *
        +------+
        | risk |
        +------+
+------------------------+
| data\companies.csv.dvc |
+------------------------+
             *
             *
             *
    +----------------+
    | climate_stress |
    +----------------+
Path                 annual_volatility_pct    average_profit_hit_pct    carbon_price_eur    confidence    one_day_var_pct    scenario                 window_days    worst_company    worst_profit_hit_pct
metrics\risk.json    16.219                   -                         -                   0.99          2.177              -                        200            -                -
metrics\stress.json  -                        22.9                      85                  -             -                  Orderly transition 2030  -              Echo Airlines    40.3
```

The 1-day Value at Risk is 2.177% and, in the stress test, Echo Airlines loses 40.3% of its
profit at a carbon price of 85 €/t. The metrics table is wide: scroll to the right to see it all.

Save everything, including the metrics:

```powershell
git add dvc.yaml dvc.lock metrics data/.gitignore
git commit -m "Add risk and climate stress stages"
uv run dvc push
```

You should see:

```text
[main ec9fa2b] Add risk and climate stress stages
 5 files changed, 95 insertions(+)
 create mode 100644 metrics/risk.json
 create mode 100644 metrics/stress.json
3 files pushed
```

## Step 8 – Change a setting and watch what reruns

This is where DVC saves time. Open `params.yaml` and change the carbon price from `85` to `150`.
Then:

```powershell
uv run dvc status
```

You should see:

```text
climate_stress:
	changed deps:
		params.yaml:
			modified:           scenario
```

DVC reports that only `climate_stress` is out of date, because only its params section changed.
Run it:

```powershell
uv run dvc repro
```

You should see:

```text
'data\prices.csv.dvc' didn't change, skipping
Stage 'returns' didn't change, skipping
Stage 'risk' didn't change, skipping
'data\companies.csv.dvc' didn't change, skipping
Running stage 'climate_stress':
> python climate_stress.py
Orderly transition 2030: worst hit Echo Airlines (71.1% of profit)
Updating lock file 'dvc.lock'
Use `dvc push` to send your updates to remote storage.
```

Only `climate_stress` runs. `returns` and `risk` are skipped. Now compare with the last commit:

```powershell
uv run dvc params diff
uv run dvc metrics diff
```

You should see:

```text
Path         Param                      HEAD    workspace
params.yaml  scenario.carbon_price_eur  85      150
Path                 Metric                  HEAD    workspace    Change
metrics\stress.json  average_profit_hit_pct  22.9    40.5         17.6
metrics\stress.json  carbon_price_eur        85      150          65
metrics\stress.json  worst_profit_hit_pct    40.3    71.1         30.8
```

In one command you see which setting changed and what it did to the results. Keep it:

```powershell
git add params.yaml dvc.lock metrics
git commit -m "Stress test at 150 EUR/t"
uv run dvc push
```

You should see:

```text
[main 3dde56a] Stress test at 150 EUR/t
 3 files changed, 9 insertions(+), 9 deletions(-)
1 file pushed
```

## Step 9 – Try an idea on a branch

Someone suggests a "greener" portfolio. Try it without disturbing the main line of work:

```powershell
git switch -c greener-portfolio
```

You should see:

```text
Switched to a new branch 'greener-portfolio'
```

In `params.yaml`, change the weights to: Alpine Steel `0.10`, Blue Wind `0.40`,
Coastal Cement `0.10`, Delta Retail `0.25`, Echo Airlines `0.15`. Then:

```powershell
uv run dvc repro               # only risk reruns
uv run dvc metrics diff main   # compare with the main branch
```

You should see:

```text
'data\prices.csv.dvc' didn't change, skipping
Stage 'returns' didn't change, skipping
Running stage 'risk':
> python risk.py
1-day VaR at 99%: 2.296% of portfolio value
Updating lock file 'dvc.lock'

'data\companies.csv.dvc' didn't change, skipping
Stage 'climate_stress' didn't change, skipping
Use `dvc push` to send your updates to remote storage.
Path               Metric                 main    workspace    Change
metrics\risk.json  annual_volatility_pct  16.219  15.018       -1.201
metrics\risk.json  one_day_var_pct        2.177   2.296        0.119
```

The annual volatility falls from 16.2% to 15.0%, but the 1-day VaR rises from 2.18% to
2.30%. Lower volatility, but a worse bad day. That's exactly the kind of finding you want recorded.
If the team likes it, commit and merge the branch. If not, throw it away:

```powershell
git restore .         # undo the uncommitted edits
git switch main
uv run dvc checkout   # data back to main's version
git branch -D greener-portfolio
```

You should see:

```text
Switched to branch 'main'
M       data\portfolio_returns.csv
Deleted branch greener-portfolio (was 3dde56a).
```

## Step 10 – Be your own colleague

A colleague needs your results. They clone the project and pull the data. Nothing is recomputed:

```powershell
cd C:\
git clone dvc-practice dvc-practice-colleague
cd dvc-practice-colleague
uv sync             # same packages as you, thanks to uv.lock
uv run dvc pull     # fetches every file the receipt names
uv run dvc status   # "Data and pipelines are up to date."
```

You should see:

```text
Cloning into 'dvc-practice-colleague'...
done.
Using CPython 3.14.4
Creating virtual environment at: .venv
Resolved 112 packages in 1ms
Installed 101 packages in 1.67s
 + aiohappyeyeballs==2.7.1
 ...                                   (about 100 lines, one per package)
A       data\companies.csv
A       data\portfolio_returns.csv
A       data\prices.csv
A       data\returns.csv
A       data\stressed.csv
5 files fetched and 5 files added
Data and pipelines are up to date.
```

`A` means DVC added the file to the colleague's folder.

The colleague now has exactly your data, byte for byte. This is how teams share
results: one person runs the pipeline and pushes, everyone else pulls.

## Exercises

Try each one before opening the answer.

<details>
<summary><b>1.</b> You change <code>confidence</code> in <code>params.yaml</code> from 0.99 to 0.95. Which stages rerun?</summary>

Only `risk`, because only it depends on the `risk` section. The 1-day VaR drops, since a 95% VaR
looks at a less extreme day than a 99% VaR.
</details>

<details>
<summary><b>2.</b> You add a comment line to <code>returns.py</code>. Which stages rerun?</summary>

`returns` reruns, because its code changed. But `risk` is **skipped**: `returns.py` produced exactly
the same `data/returns.csv` as before, so its hash is unchanged. DVC follows content, not
timestamps. This surprises many people, and it is one of DVC's biggest time savers.
</details>

<details>
<summary><b>3.</b> You need the version-1 prices as a separate file, without changing your workspace. How?</summary>

Find the commit with `git log --oneline` (the one named "Add input data, version 1"), then:

```powershell
uv run dvc get . data/prices.csv --rev <commit-id> -o prices_v1.csv
```

It prints nothing. A new file `prices_v1.csv` appears in the folder, with the 250 days of version 1.

`dvc get` downloads one file at one version. It also works with a GitHub URL instead of `.`,
which is useful for people who don't want to clone a whole repository.
</details>

<details>
<summary><b>4.</b> A colleague runs <code>dvc pull</code> and gets "missing cache" errors. What happened?</summary>

You committed the receipt (`dvc.lock` or a `.dvc` file) but forgot `dvc push`. The receipt points
to data that isn't on the remote yet. Run `dvc push` and ask them to pull again.
</details>

<details>
<summary><b>5.</b> Someone edits <code>data/returns.csv</code> by hand. What does <code>dvc status</code> say, and how do you fix it?</summary>

It reports that the output of `returns` was modified. Never keep hand edits to outputs.
`dvc checkout data/returns.csv` restores the recorded version, or `dvc repro --force returns`
recomputes it.
</details>

## In short

- **`dvc add`** versions a data file. git keeps only a small pointer file (`.dvc`) with its hash.
- **`dvc push` and `dvc pull`** share data through storage. **`git checkout` then `dvc checkout`** takes you to any past version.
- **A stage** lists what it reads (`deps`), its settings (`params`) and what it writes (`outs`, `metrics`). `dvc repro` reruns only what changed.
- **`dvc params diff` and `dvc metrics diff`** show what a change did, between commits or branches.

---

← [Previous: How DVC works](1-how-dvc-works.md) · [Next on track 1: Bring an existing project into git and DVC](4-existing-project.md) → · [Next on track 2: DVC in your own project](3-your-own-project.md) →
