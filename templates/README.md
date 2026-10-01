# Templates

Files to copy into your own repository. Rename the pipelines, commands and settings to match yours.

From [DVC in your own project](../docs/3-your-own-project.md), for the invented project *greenfin-risk*:

| File | Copy it to | What it is |
|---|---|---|
| `dvc.yaml` | `pipelines\<pipeline>\dvc.yaml` | A full example pipeline: download → prepare → cash flow → valuation → ratings → report → publish |
| `config.yaml` | `pipelines\<pipeline>\config.yaml` | The settings the pipeline depends on, key by key |
| `run.py` | `tools\run.py` | A wrapper that runs DVC for one pipeline at a time (for repositories with several pipelines) |
| `dvc-check.yml` | `.github\workflows\dvc-check.yml` | A GitHub Actions check that pulls the data and fails if a `dvc.lock` is out of date |
| `gitignore.txt` | `.gitignore` | Keeps environments, credentials, Python caches, Excel lock files and editor files out of git |
| `gitattributes.txt` | add the lines to `.gitattributes` | Stops git on Windows from changing metrics files, so a fresh clone matches `dvc.lock` |

From [Bring an existing project into git and DVC](../docs/4-existing-project.md) and the
[worked example](../docs/5-worked-example.md), for the invented project *climate-price-paths*:

| File | Copy it to | What it is |
|---|---|---|
| `README-template.md` | `README.md` | A README with the four questions every project should answer |
| `paths_example.py` | the top of each script | Paths that work on every computer |
| `climate-price-paths/` | see its [README](climate-price-paths/README.md) | A working two-stage pipeline, and a script that delivers a version to S3 with a record |

From the [Going further](../README.md#going-further) pages:

| File | Copy it to | What it is |
|---|---|---|
| `experiments/` | a new practice folder | One model script, its settings and an invented panel, to practise [experiments](../docs/experiments.md) |
| `run_pipeline.py` | the repository root | A thin runner that keeps familiar commands while DVC does the work ([Replace a home-made runner](../docs/replace-a-runner.md)) |
| `check_handoff.py` | the repository root | Checks that a hand-off file has the expected columns and keys ([Several owners](../docs/several-owners.md)) |
| `CODEOWNERS.txt` | `.github/CODEOWNERS` | Sends each change to the owner of that part for review ([Several owners](../docs/several-owners.md)) |
