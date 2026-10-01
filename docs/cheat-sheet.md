[Home](../README.md) › Cheat sheet

# Cheat sheet

*The commands of the tutorial, on one page.*

## Run pipelines

| Task | Command |
|---|---|
| Start DVC in a git repository | `uv run dvc init` |
| Version a data file | `uv run dvc add <file>`, then `git add <file>.dvc` and commit |
| Add a pipeline stage | `uv run dvc stage add -n <name> -d <dep> -p <params> -o <out> -M <metric> <command>` |
| Run what changed | `uv run dvc repro` |
| What is out of date | `uv run dvc status` |
| Draw the pipeline | `uv run dvc dag` |
| Compare settings / results | `uv run dvc params diff`, `uv run dvc metrics diff [branch]` |
| Send / get data | `uv run dvc push`, `uv run dvc pull` |
| Make data match the current commit | `uv run dvc checkout` |
| Download one file at one version | `uv run dvc get <repo> <path> --rev <tag or commit>` |

### Bring an existing project in, and work with branches

| Task | Command |
|---|---|
| Create the standard folders | `mkdir scripts, data\raw, data\reference, outputs, metrics, docs` |
| Record the Python version and packages | `uv init --bare`, `uv python pin <version>`, `uv add <packages>` |
| Version a whole data folder | `uv run dvc add data/raw` (again after any change in it) |
| Start a piece of work | `git switch main`, `git pull`, `git switch -c <short-name>` |
| Share the branch | `git push -u origin <short-name>`, then open a pull request on GitHub |
| After the merge | `git switch main`, `git pull` |
| Tag a delivered version | `git tag <name>`, `git push origin <name>` |

### Experiments

| Task | Command |
|---|---|
| Queue an experiment with other settings | `uv run dvc exp run --queue -n <name> -S <section.key>=<value>` |
| Run all queued experiments | `uv run dvc exp run --run-all` |
| Compare experiments | `uv run dvc exp show --only-changed` |
| What changed between two experiments | `uv run dvc exp diff <name> <name>` |
| Bring an experiment into your folder | `uv run dvc exp apply <name>` |
| Turn the winner into a branch | `uv run dvc exp branch <name> <branch>` |
| Share an experiment | `uv run dvc exp push origin <name>`, `uv run dvc exp pull origin <name>` |
| Remove experiments | `uv run dvc exp remove <name>`, or `-A` for all |

### Several stages and owners

| Task | Command |
|---|---|
| Bring one stage up to date (and what it needs) | `uv run dvc repro <stage>` |
| Get one stage's results without rerunning it | `uv run dvc pull <stage>` |
| What would run | `uv run dvc repro --dry` |
| Check a hand-off file | `uv run python check_handoff.py <file>` |
| Check that `.env` is ignored | `git check-ignore -v .env` |

### Setting up storage

| Task | Command |
|---|---|
| Add a remote (default) | `uv run dvc remote add -d <name> s3://<bucket>/<folder>` |
| Add a remote (not default) | `uv run dvc remote add <name> s3://<bucket>/<folder>` |
| Set its region | `uv run dvc remote modify <name> region <region>` |
| Use your AWS profile, outside git | `uv run dvc remote modify --local <name> profile <profile>` |

### With the wrapper (several pipelines in one repository)

| Task | Command |
|---|---|
| Latest results | `uv run tools/run.py <pipeline> pull` |
| What is out of date | `uv run tools/run.py <pipeline> status` |
| What would rerun | `uv run tools/run.py <pipeline> dry` |
| Run | `uv run tools/run.py <pipeline> repro` |
| Share results | `uv run tools/run.py <pipeline> push` |
| Old release in its own folder | `git worktree add ..\<folder> <tag>`, then `pull` there |

---

← [Back to the start page](../README.md)
