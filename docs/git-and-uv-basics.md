[Home](../README.md) › Git and uv basics

# Git and uv basics

*For people new to git, before you start the tutorial. It takes about 15 minutes.*

**Good at git?** Skip this page.

You only need a few git and uv commands. This page covers exactly those, and nothing more.

## Git in five minutes

You need only a handful of git commands for this tutorial:

| Command | What it does |
|---|---|
| `git status` | Shows which files changed. Run it often, it never breaks anything. |
| `git add <file>` | Puts a file "in the basket" for the next save. |
| `git commit -m "message"` | Saves everything in the basket as a new version, with a message. |
| `git log --oneline` | Lists past versions (commits), newest first. |
| `git switch -c <name>` | Creates a branch: a separate line of work you can throw away. |
| `git switch <name>` | Moves to an existing branch. |
| `git pull` / `git push` | Gets / sends commits from / to GitHub. |

Think of a commit as a named snapshot of the project. A branch is a series of snapshots that
doesn't disturb anyone else until it is merged.

## uv in five minutes

`uv` is the tool that gives each project its own Python and packages. It replaces `pip`, `venv`
and separate Python installers with one fast command.

Four ideas are enough:

- **Environment.** A private folder, `.venv`, holding one project's Python and packages. Projects
  don't interfere with each other, and nothing is installed "globally" on your computer.
- **`pyproject.toml`.** The project's list of the packages it needs, written by people.
- **`uv.lock`.** The exact version of every package, written by uv. It's committed to git, so
  everyone on the team gets identical packages. It's the same idea as `dvc.lock`, but for code.
- **Workspace.** A bigger repository can contain several packages (for example `packages/cash_flow`,
  `packages/valuation`) that share one environment and one `uv.lock`.

| Command | What it does |
|---|---|
| `uv sync` | Creates or updates `.venv` so it matches `uv.lock` exactly. Run it after cloning and after every `git pull`. In a workspace, add `--all-packages`. |
| `uv run <command>` | Runs a command inside the project's environment. It syncs first if needed, so you never have to "activate" anything. |
| `uv run --env-file .env <command>` | The same, but first loads the variables from `.env`, such as AWS keys. |
| `uv add <package>` | Adds a package to `pyproject.toml` and `uv.lock`. In a team, do this in a pull request, because it changes everyone's environment. |
| `uv tree` | Shows which packages are installed and why. |
| `uv python install 3.12` | Installs a Python version, if a project needs one you don't have. |

In this tutorial, every `dvc` and `python` command starts with `uv run`:

```powershell
uv run dvc status          # runs DVC inside the project's environment
uv run make_data.py        # runs a Python script the same way
```

There is nothing to activate, and `uv run` always checks first that your packages match `uv.lock`.

## Done

Start the tutorial: [1. How DVC works](1-how-dvc-works.md).

---

← [Back to the start page](../README.md)
