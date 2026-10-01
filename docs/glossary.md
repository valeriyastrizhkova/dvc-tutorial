[Home](../README.md) › Glossary

# Glossary

*Every term the tutorial uses, in plain words.*

| Word | Meaning |
|---|---|
| **AWS profile** | A named set of your AWS keys, stored once with `aws configure --profile <name>`, so they never appear in a project. |
| **Branch** | A separate line of work in git. Short branches, named after what they do, are merged into `main` through pull requests. |
| **Bucket (S3)** | A storage space in Amazon S3, like a shared drive. DVC keeps data versions in a folder of a bucket. |
| **Cache** | The hidden folder (`.dvc/cache`) where DVC keeps a copy of each data version on your computer. |
| **Checkout** | `git checkout` moves code and pointers to a version; `dvc checkout` makes the data match. |
| **Clone** | A full copy of a repository on your computer, made with `git clone`. |
| **CODEOWNERS** | A GitHub file listing who owns which folders. Pull requests that change them automatically ask those people for a review. |
| **Commit** | A named snapshot of the project in git. |
| **DAG** | The picture of a pipeline: which stage feeds which. `dvc dag` draws it. (It stands for "directed acyclic graph".) |
| **Dependency (dep)** | A file or folder a stage reads. If it changes, the stage reruns. |
| **`.dvc` file** | A small pointer file next to a data file you added with `dvc add`. It holds the data's hash, and git keeps it. |
| **`dvc.yaml`** | The recipe: the list of stages, with what each one runs, reads and writes. |
| **`.env`** | A file of credentials and private settings, read by your scripts. It must never be in git. |
| **Experiment** | A run of the pipeline with different settings, recorded by DVC and compared with others in `dvc exp show`. |
| **Frozen stage** | A stage `dvc repro` never runs. Useful for publishing. |
| **Hand-off file** | One part's output that another part of the pipeline reads, such as a projection used by the next model. |
| **Hash (MD5)** | A short code computed from a file's content. It changes if one byte changes. |
| **Lock file (`dvc.lock`)** | The receipt: the hashes of every dependency and output of the last run. |
| **Lock file (Excel)** | A temporary file such as `~$prices.xlsx` that Excel creates while a file is open. Never commit it. |
| **Merge** | Bringing the changes of one branch into another, usually into `main` through a pull request. |
| **Metric** | A small results file kept in git (`cache: false`) so changes show in pull requests. |
| **Output (out)** | A file or folder a stage produces. DVC stores and versions it. |
| **Params** | Settings from a config file that a stage depends on, key by key. |
| **Parquet** | A compact, fast file format for tables. Good for files that only your code reads. |
| **Pipeline** | Stages linked by their dependencies and outputs, described in `dvc.yaml`. |
| **Pull / push** | Get data from / send data to the remote. |
| **Pull request** | A request, on GitHub, to merge a branch into `main`. Colleagues review the changes there before they're merged. |
| **`pyproject.toml`** | The list of Python packages a project needs, written by people (with `uv add`). |
| **Queue** | A list of experiments waiting to run: `dvc exp run --queue` adds one, `dvc exp run --run-all` runs them. |
| **Remote** | Shared storage for data versions, such as an S3 bucket. |
| **Repository folder** | The top folder of a git repository. Scripts find it with `Path(__file__).resolve().parents[1]`, so paths work on every computer. |
| **Repro** | "Reproduce": run every stage whose dependencies changed. |
| **Snapshot date** | A date in the config that pins which version of an external download a stage uses. |
| **Stage** | One step of a pipeline: a command with its dependencies and outputs. |
| **Tag** | A permanent name for a commit, such as a release: `corporate/2026.09`. |
| **`uv.lock`** | The exact version of every package, written by uv, so everyone gets the same environment. |
| **Workspace** | Your project folder as it is right now, including changes you haven't committed yet. |
| **Worktree** | A second folder showing another commit of the same git repository. |

---

← [Back to the start page](../README.md)
