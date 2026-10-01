[Home](../README.md) › Setup

# Set up your computer

Do steps 1 to 6 once. Steps 7 and 8 are optional: use them if you work in VS Code or Spyder.

1. [Open a terminal](#step-1--open-a-terminal)
2. [Choose where your projects live](#step-2--choose-where-your-projects-live)
3. [Install uv](#step-3--install-uv)
4. [Store your storage keys](#step-4--store-your-storage-keys)
5. [Install git](#step-5--install-git)
6. [Allow PowerShell to run scripts](#step-6--allow-powershell-to-run-scripts)
7. [Optional: use VS Code](#step-7--optional-use-vs-code)
8. [Optional: use Spyder](#step-8--optional-use-spyder)

## Good at git: quick checklist

> **Good at git?** Check these six points, then [start the tutorial](1-how-dvc-works.md).
>
> 1. git works in PowerShell, and `git config --global core.longpaths true` is set.
> 2. uv is installed: `uv --version`.
> 3. Your repositories are in a short path such as `C:\projects`, **not** in a OneDrive folder ([step 2](#step-2--choose-where-your-projects-live)).
> 4. PowerShell can run scripts ([step 6](#step-6--allow-powershell-to-run-scripts)).
> 5. The AWS CLI is installed and your keys are stored under a profile ([step 4](#step-4--store-your-storage-keys)).
> 6. You have no stale `AWS_*` variables in your terminal: `Get-ChildItem Env:AWS*` shows nothing.
>
> Using VS Code or Spyder? Also read [step 7](#step-7--optional-use-vs-code) or [step 8](#step-8--optional-use-spyder): each takes two minutes.

## Step 1 – Open a terminal

A terminal is a window where you type commands instead of clicking. On Windows we use
**PowerShell**: press the Windows key, type `PowerShell` (or `Terminal` on Windows 11), press Enter.

A handy shortcut: open a folder in File Explorer, click the address bar, type `powershell` and
press Enter. A terminal opens already inside that folder.

These commands are enough to move around:

```powershell
pwd          # where am I?
ls           # what is in this folder?
cd folder    # go into a folder;  cd ..  goes up one level
explorer .   # open the current folder in File Explorer
```

## Step 2 – Choose where your projects live

Create one folder for all your repositories, directly on the C: drive:

```powershell
mkdir C:\projects
```

**Don't put repositories on the Desktop, in Documents or anywhere OneDrive syncs.** On many
company laptops those folders are synced by OneDrive, which locks files while it uploads them,
duplicates DVC's cache to the cloud, and adds to Windows' path length limits. All three cause
confusing DVC errors.

## Step 3 – Install uv

`uv` installs Python and a project's packages for you. This tutorial uses it everywhere, and it
works the same for your own projects.

```powershell
winget install --id astral-sh.uv -e
# or, if winget isn't available:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close and reopen PowerShell, then check:

```powershell
uv --version
```

## Step 4 – Store your storage keys

Shared data is kept in cloud storage. In this tutorial that's an Amazon S3 bucket. To reach it you
need your own access keys: ask your cloud administrator or team lead for them.

Install the AWS command-line tool:

```powershell
winget install --id Amazon.AWSCLI -e
```

Close and reopen PowerShell, then store your keys under a *profile*, a name for this set of keys.
Use the profile name your team agrees on; this tutorial uses `team`:

```powershell
aws configure --profile team
```

It asks four questions: paste your access key ID and secret access key, type your region (for
example `eu-west-1`), and press Enter for the last one. Your keys are now saved in your Windows
user folder, never in a project.

**One trap to know.** An AWS key set directly in the terminal wins over your profile. If you ever
set `$env:AWS_ACCESS_KEY_ID` in PowerShell, or have it in your Windows user variables, you'll get
`403 Forbidden` errors. Check and clear them:

```powershell
Get-ChildItem Env:AWS*     # lists any AWS variables set in this terminal
Remove-Item Env:AWS_*      # clears them for this terminal
```

If they come back in every new terminal, they are saved in Windows: open *Edit environment
variables for your account* from the Start menu and delete them there.

## Step 5 – Install git

Download **Git for Windows** from [git-scm.com](https://git-scm.com/downloads) and install it
with the default options, or install it from PowerShell:

```powershell
winget install --id Git.Git -e
```

Close and reopen PowerShell, then check it works:

```powershell
git --version
```

Tell git who you are. You only do this once per computer:

```powershell
git config --global user.name "Your Name"
git config --global user.email "you@company.com"
```

Data projects often have long file paths, which Windows refuses by default. Allow them once:

```powershell
git config --global core.longpaths true
```

## Step 6 – Allow PowerShell to run scripts

PowerShell blocks scripts by default, including the ones this tutorial uses. Allow them for your
own account, once:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

If company policy blocks that, use the **Command Prompt** instead (type `cmd` in the Start menu).
Every command in this tutorial works there too.

## Step 7 – Optional: use VS Code

You can do the whole tutorial inside VS Code. On Windows, its built-in terminal **is** PowerShell,
so every command in this tutorial works there exactly as written. VS Code adds buttons for some
tasks: the tutorial mentions them with **In VS Code:** next to the commands. Use whichever you
prefer; the commands always work.

**Install VS Code and two extensions.** If you don't have VS Code yet:

```powershell
winget install --id Microsoft.VisualStudioCode -e
```

Then open the Extensions view (Ctrl+Shift+X) and install:

- **Python**, by Microsoft: finds your project's `.venv` and uses it automatically.
- **DVC**, by Iterative: shows the files DVC tracks and adds DVC commands to VS Code.

**Open a project and a terminal.**

1. *File → Open Folder* and choose the project folder, for example `C:\dvc-practice`.
2. *Terminal → New Terminal* (or Ctrl+`). A PowerShell terminal opens **already inside the project
   folder**, so you never need to `cd` into it.
3. If VS Code asks which Python to use, choose the one in `.venv`. If it doesn't ask, press
   Ctrl+Shift+P, type **Python: Select Interpreter**, and pick `.venv`. From then on, new
   terminals activate the environment automatically.

**Three places you'll use:**

| Where | How to open it | What it does |
|---|---|---|
| **Source Control** | Ctrl+Shift+G | Shows changed files, commits them with a message, and pulls and pushes with the **Sync Changes** button. |
| **Timeline** | Bottom of the Explorer (Ctrl+Shift+E), with a file selected | Lists every saved version of that file, with its message. The same as `git log`, without typing. |
| **Command Palette** | Ctrl+Shift+P | Runs any command by name, such as **DVC: Pull** or **DVC: Push**. |

The script permission from [step 6](#step-6--allow-powershell-to-run-scripts) applies inside VS Code too,
because it's the same PowerShell.

## Step 8 – Optional: use Spyder

If you write your code in **Spyder**, you can keep it: point Spyder at your project's Python
environment, and run git and DVC commands in PowerShell next to it.

1. **Add Spyder's helper package to the project**, once, in PowerShell:

   ```powershell
   uv add --dev spyder-kernels
   ```

   If Spyder later says the version of `spyder-kernels` doesn't match, it names the version it
   needs: install exactly that one, for example `uv add --dev "spyder-kernels==3.0.*"`.

2. **Point Spyder at the project's Python.** In Spyder: *Tools → Preferences → Python interpreter
   → Use the following Python interpreter*, and choose `.venv\Scripts\python.exe` inside your
   project folder. Restart the console (*Consoles → Restart kernel*).

3. **Run git and DVC in PowerShell**, opened in the project folder. Spyder runs your scripts;
   PowerShell runs `git`, `uv run dvc repro` and the other commands.

Two habits matter especially with Spyder:

- **Don't rely on Spyder's working folder.** Start every path from the repository folder, as on
  [page 4, section 5](4-existing-project.md#5-paths-that-work-on-every-computer). Then your scripts
  run the same in Spyder, in PowerShell and in DVC.
- **Don't commit the files Spyder creates**: an empty file with only a header, or the
  `.spyproject` folder. The [`.gitignore` template](../templates/gitignore.txt) already ignores
  `.spyproject`.

## Done

New to git? Read [Git and uv basics](git-and-uv-basics.md) first. Then start the tutorial:
[1. How DVC works](1-how-dvc-works.md).

---

← [Back to the start page](../README.md)
