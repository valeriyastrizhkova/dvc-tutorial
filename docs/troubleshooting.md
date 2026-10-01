[Home](../README.md) › When something goes wrong

# When something goes wrong

*Find what you see in the first column, then do what the last column says. For every track.*

| What you see | Why | What to do |
|---|---|---|
| `403 Forbidden` or `Access Denied` on pull or push | DVC has no credentials, the wrong ones, or an old `AWS_*` variable overrides them | Check your profile ([Setup, step 4](setup.md#step-4--store-your-storage-keys)) and that DVC uses it ([DVC in your own project, section 2](3-your-own-project.md#2-add-dvc-to-an-existing-repository)). Clear old variables with `Remove-Item Env:AWS_*`. |
| "running scripts is disabled on this system" | PowerShell blocks scripts, such as the one VS Code runs to activate `.venv` | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, or use Command Prompt ([Setup, step 6](setup.md#step-6--allow-powershell-to-run-scripts)). |
| "The process cannot access the file because it is being used by another process" | A data file is open in Excel, or shown in File Explorer's preview pane | Close Excel and the preview pane, then run the command again. |
| Random "permission denied", or files reappearing | The repository is inside a OneDrive folder | Move it to `C:\projects` ([Setup, step 2](setup.md#step-2--choose-where-your-projects-live)). |
| Several pipelines run at once | You ran `dvc repro` at the root of a multi-pipeline repository | Use the wrapper ([DVC in your own project, section 4](3-your-own-project.md#4-several-pipelines-in-one-repository)). |
| `missing cache` / some files fail to pull | Someone committed a receipt but didn't push the data | Ask them to push. |
| `Unable to acquire lock` | Another DVC command is running, or one crashed | Close other terminals running DVC and try again. If nothing is running, the error message names the lock file; delete it. |
| A stage doesn't rerun though you changed something | The file you changed isn't in that stage's `deps` | Add it to `deps`, and tell the team: their results are stale too. |
| "Stage is frozen" | You tried to run the publish stage | By design. Publishing happens in the release process. |
| A merge conflict in `dvc.lock` | Two branches ran the pipeline | Don't edit hashes by hand. Keep one side, then rerun `repro` so the lock matches real data. |
| Your disk is full | The cache keeps every version you pulled | `uv run dvc gc --workspace` removes local versions not used by your current checkout. **Never** add `--cloud`: that deletes data from the shared remote. |
| "Filename too long" | Windows' default path limit | `git config --global core.longpaths true`, and keep repositories in a short path like `C:\projects`. |

---

← [Back to the start page](../README.md)
