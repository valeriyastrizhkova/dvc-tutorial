[Home](../README.md) › Both tracks › Page 6

# 6. Good habits

> **For you if** you've finished your track, or you want a reminder of what matters most.
>
> **You'll learn** the habits that keep a project working, grouped into data, code and files, working with others, and safety on Windows.
>
> **Time:** about 10 minutes.

Print this page, or keep it open: it's the whole tutorial in eighteen lines.

## Data

1. **Never put data in git.** If a file is bigger than a few hundred kilobytes, it belongs to DVC.
2. **Never edit an output by hand.** Change the code or a setting, then `repro`.
3. **Push after you commit a receipt.** A `dvc.lock` or `.dvc` file without pushed data is a broken
   promise to your colleagues.
4. **After switching branches or commits, pull (or `dvc checkout`).** Otherwise your data
   doesn't match your code.
5. **Pin downloads with a snapshot date.** Then you always know which data a result used.

## Code and files

6. **Put settings in a config file, not in the code.** Then DVC can track exactly which settings a
   stage uses, and `params diff` shows what changed.
7. **No personal paths in the code.** No `C:\Users\...` and no `os.chdir()`: start every path from
   the repository folder ([page 4, section 5](4-existing-project.md#5-paths-that-work-on-every-computer)).
8. **One name per file, for ever.** No `_V2`, `_final`, `- Copy` or initials: git and DVC keep the
   versions ([page 4, section 6](4-existing-project.md#6-stop-keeping-versions-in-file-names)).
9. **One script per model, not one copy per idea.** Vary settings in `params.yaml`, and compare the
   runs as experiments ([Track experiments with DVC](experiments.md)).
10. **Keep small results as metrics.** They show up in every pull request.

## Working with others

11. **`main` is the truth.** Work on short, named branches, and bring changes back through pull
    requests ([page 4, section 11](4-existing-project.md#11-work-with-branches-from-now-on)).
12. **Commit at the end of every working session**, with a message that says what changed and why.
13. **Agree on one commit rule** (A or B, [page 3, section 5](3-your-own-project.md#what-do-i-commit-after-a-run)) and write it down.
14. **Deliver with a record.** Never send a result by hand: tag it, or publish it to a versioned
    folder ([page 5, section 7](5-worked-example.md#7-deliver-a-version-with-a-record)).

## Safety on Windows

15. **Keep repositories in `C:\projects`, outside OneDrive.**
16. **Close Excel before `pull`, `checkout` or `repro`.** Windows won't let DVC replace a file that
    Excel has open. To look at results, copy the file somewhere else first.
17. **Check that `.env` is really ignored**: `git check-ignore -v .env` must print a rule.
18. **When in doubt, `status` first.** It never changes anything.

## Apply it to your own repository

The best way to make all this stick is to use it on your own work. Take one of your repositories,
ideally with a colleague, and go through the
[checklist on page 4](4-existing-project.md#12-check-your-repository). For each "no":

1. open a short branch for it, for example `remove-personal-paths`,
2. fix it, following the page and section the checklist points to,
3. open a pull request, and ask your colleague to review it.

When every box is ticked, do the final test: your colleague clones the repository and runs
`uv sync`, `uv run dvc pull` and `uv run dvc repro`, without your help.

## You've finished the tutorial

Three pages go further, when you need them:

- [Track experiments with DVC](experiments.md): many variations of a model, compared in one table
- [Replace a home-made runner with DVC](replace-a-runner.md): when a `run_all.py` runs everything
- [A pipeline owned by several people](several-owners.md): safe hand-offs and the right reviewers

- Keep the [cheat sheet](cheat-sheet.md) at hand.
- If something goes wrong, see [When something goes wrong](troubleshooting.md).

---

← Previous: [Worked example](5-worked-example.md) (track 1) · [DVC in your own project](3-your-own-project.md) (track 2) · [Next: Track experiments with DVC](experiments.md) →
