[Home](../README.md) › Going further › Several owners

# A pipeline owned by several people

> **For you if** your pipeline has parts that different people own: one person builds the macro projections, another fits the credit scores on them, a third prices loans from the scores. Each part hands files to the next.
>
> **You'll learn** to make hand-offs between parts safe, check them automatically, send each change to the right reviewer, and work in parallel.
>
> **Time:** about 30 minutes.
>
> **Before this page:** [Replace a home-made runner with DVC](replace-a-runner.md), or [page 5](5-worked-example.md), so the pipeline is already in `dvc.yaml`.

**On this page:**

- [1. The risks](#1-the-risks)
- [2. Make every hand-off explicit](#2-make-every-hand-off-explicit)
- [3. Check the hand-offs automatically](#3-check-the-hand-offs-automatically)
- [4. Send every change to the right reviewer](#4-send-every-change-to-the-right-reviewer)
- [5. Work in parallel, without rerunning each other's parts](#5-work-in-parallel-without-rerunning-each-others-parts)
- [6. Change a hand-off safely](#6-change-a-hand-off-safely)
- [7. Checklist](#7-checklist)

## 1. The risks

When several people share a pipeline, three things go wrong more than anything else:

- **Someone changes a hand-off file**, renames a column or changes a unit, and the next part breaks,
  or worse, keeps running with wrong numbers.
- **A change in one part is merged without its owner seeing it.**
- **Everyone reruns everyone else's part** to test their own, and waits.

Each section below removes one of them.

## 2. Make every hand-off explicit

A **hand-off file** is one part's output that another part reads, such as
`data/intermediate/macro_projection.csv`. Two things make hand-offs safe.

**In `dvc.yaml`**, each hand-off is an `outs` of the stage that writes it, and a `deps` of every
stage that reads it ([Replace a home-made runner, step 2](replace-a-runner.md#step-2-write-one-stage-per-script)).
Then DVC knows the order, and reruns the next part whenever the hand-off changes.

**In `docs/handoffs.md`**, write down what each hand-off contains: one short table per file.

```markdown
## data/intermediate/macro_projection.csv

Written by: macro_project (owner: Alice). Read by: scores_project, pricing_fit.

| Column | Meaning | Unit |
|---|---|---|
| scenario | climate scenario name | |
| country | ISO3 code | |
| year | 2024 to 2050 | |
| gdp_growth | real GDP growth | % per year |
| debt_ratio | public debt | % of GDP |

One row per scenario, country and year.
```

It takes ten minutes, and it's the document everyone opens when a number looks strange.

## 3. Check the hand-offs automatically

Documentation can drift, so let the pipeline check the hand-offs too.
[`templates/check_handoff.py`](../templates/check_handoff.py) checks a file's columns, and that
its key columns (here scenario, country and year) are never empty or repeated. Run it at the end of
the stage that writes the hand-off:

```yaml
  macro_project:
    cmd:
    - python scripts/01_macro/02_project.py
    - python check_handoff.py data/intermediate/macro_projection.csv
    deps:
    - scripts/01_macro/02_project.py
    - check_handoff.py
    ...
    outs:
    - data/intermediate/macro_projection.csv
```

DVC runs the two commands one after the other. If the macro script ever writes a file without
`debt_ratio`, the stage fails right there, with a
message naming the missing column, instead of the credit-score part failing later with a confusing
error. Edit the `HANDOFFS` list at the top of the script to match your `docs/handoffs.md`.

## 4. Send every change to the right reviewer

GitHub can ask the owner of a part to review every pull request that touches it. Copy
[`templates/CODEOWNERS.txt`](../templates/CODEOWNERS.txt) to `.github/CODEOWNERS`, and replace the
names with your colleagues' GitHub user names:

```
*                       @team-lead

/scripts/01_macro/         @alice
/scripts/02_credit_scores/ @bruno
/scripts/03_loan_pricing/  @chloe

/dvc.yaml               @alice @bruno @chloe
/docs/handoffs.md       @alice @bruno @chloe
```

The last lines matter most: `dvc.yaml` and the hand-off documentation connect the parts, so every
owner reviews changes to them.

To make the review required rather than just requested, an administrator of the repository can add
a rule for `main`: *Settings → Branches → Add branch protection rule*, then tick **Require a pull
request before merging** and **Require review from Code Owners**.

## 5. Work in parallel, without rerunning each other's parts

When Bruno works on the credit scores, he doesn't need to rerun Alice's macro projections. He
**pulls** them instead:

```powershell
git switch main
git pull
uv run dvc pull macro_project
git switch -c better-score-model
```

`dvc pull macro_project` downloads only that stage's outputs, exactly as recorded in `dvc.lock`.
Bruno then works on his part, and `uv run dvc repro scores_project` reruns only his stages.

**One `dvc.yaml`, or one per part?** One file at the repository root is the simplest, and it shows
the whole pipeline in one place. If the parts grow large, each can have its own `dvc.yaml` in its
folder, such as `scripts/02_credit_scores/dvc.yaml`. DVC finds them all, and a stage is then named
with its file: `uv run dvc repro scripts/02_credit_scores/dvc.yaml:scores_project`.

## 6. Change a hand-off safely

Sometimes a hand-off has to change: a new column, a new unit, a new name. Do it in this order, so
the next part never breaks:

1. **Agree on it first**, in a pull request that only changes `docs/handoffs.md`. Every owner
   reviews it, thanks to `CODEOWNERS`.
2. **Add before you remove.** Write the new column next to the old one, and update
   `check_handoff.py`.
3. **The readers move to the new column**, each in their own pull request.
4. **Then remove the old column**, in a last pull request.

In every one of these pull requests, run the whole pipeline with `uv run dvc repro`, and look at
`uv run dvc metrics diff`: it shows at once whether the downstream results moved.

## 7. Checklist

- [ ] Every hand-off file is an `outs` of one stage, and a `deps` of the stages that read it
- [ ] `docs/handoffs.md` describes each hand-off: columns, units, keys, owner
- [ ] The stage that writes a hand-off checks it with `check_handoff.py`
- [ ] `.github/CODEOWNERS` names the owner of each part, and every owner for the shared files
- [ ] Owners pull each other's results with `uv run dvc pull <stage>` instead of rerunning them

## In short

- **Every hand-off is an output of one stage and an input of the next**, described in `docs/handoffs.md`.
- **The stage that writes a hand-off checks it**, so a missing column fails early, with a clear message.
- **`CODEOWNERS` asks the owner of each part to review changes** to it, and every owner for the shared files.
- **Pull, don't rerun, each other's results**, and change a hand-off in four steps: agree, add, move, remove.

---

← [Previous: Replace a home-made runner with DVC](replace-a-runner.md) · [Home](../README.md)
