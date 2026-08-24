---
type: workflow
title: Prune archived decisions
description: Permanently remove decision records that have been archived longer than the retention period. Only reaches `archived/`, never a live decision. Rarely the right call.
---

# Prune archived decisions

**The only workflow in this bundle that deletes anything, and it is deliberately
awkward to reach.**

Everything else here archives. A superseded decision moves to `archived/`, stops
being loaded, and stays findable — which answers the context cost that makes
people want to delete records in the first place. **If that is what you are
after, you do not need this workflow**, and [[record-decision]] already did it.

This exists for the narrow case past that: a record archived long enough that
nothing could still be resting on it, in a project that has decided it does not
want to carry it.

## What it will not touch

**Only `archived/`.** A record still in `.luma/records/decisions/` is not
reachable from this workflow at all — not with a flag, not with confirmation, not
by naming the file. Archiving first is a separate act with its own reasoning, and
collapsing the two would make deleting a live decision one step away from routine.

**Only past the retention period.** Recently archived is not eligible, however
obviously spent it looks.

**Never `superseded_by` targets.** A record something points at stays, whatever
its age. Deleting it breaks the chain that explains why the current position
exists — see step 5.

## 1. Read the retention period, and stop if there is not one

```toml
# .luma/config/decision-records.toml — committed
[require]
archived_retention = "3y"
```

**`[require]` rather than `[defaults]`**, because a locally-overridable retention
period means one operator can delete what another could not, from the same commit.
That is a correctness problem rather than a preference.

*Where settings live and how the layers resolve is the `luma/luma-config` bundle's
subject. **This bundle does not depend on it** — the file above is plain TOML and
reading one key from it needs nothing installed.*

**Absent means this workflow does not run.** Not *fall back to a sensible
default*: report what the setting is, what it would do, and stop.

**Because you declare to gain a capability, never to lose one.** A default
retention would hand every project that never thought about this a working delete
path, which is exactly backwards for the one destructive operation in the bundle.
Setting the value is the project saying *we want to be able to do this*, and that
statement should be in a committed file with somebody's name on the commit.

**Three years is a reasonable first value and not a recommendation to inherit.**
The right number depends on how long a project's decisions stay load-bearing, and
a project that cannot say is a project that should leave the setting out.

## 2. Find what is eligible

**The clock runs from `archived`, not from `decided`.** A decision settled in 2019
and retired last month was live for six years; the retention period is measuring
how long it has been *spent*.

```yaml
lifecycle_status: archived
archived: 2022-03-14        # the clock this workflow reads
```

**Where `archived` is absent, recover it from the move into `archived/`:**

```sh
git log --diff-filter=A --format=%ad --date=short -- \
  .luma/records/decisions/archived/ADR-0004-<slug>.md | tail -1
```

**Where neither gives a date, the record is not eligible.** Not *probably old
enough* — unestablished. A check that cannot be performed is a failure rather than
a pass, which is how every other rule in this bundle resolves.

**Say how many were excluded for want of a date**, and offer to backfill
`archived` on them instead. That is the useful outcome of a run that deletes
nothing.

## 3. Sort by `archived_reason` before reading anything

**The four values are not equally prunable, and sorting on them saves reading
records that were never candidates.**

| | |
| --- | --- |
| `noise` | **The clearest case.** It was never a decision, so nothing can be resting on it |
| `retired` | **Ordinary.** Finished business with no successor. The record is history, and whether history is worth keeping is the actual question this workflow asks |
| `superseded` | **Usually keep.** The successor explains itself by reference to this. Step 5 will normally disqualify it anyway |
| `invalidated` | **Do not propose.** This marks a gap — the project used to have an answer and no longer does. Deleting it deletes the evidence that something needs re-deciding |
| absent | Treat as `retired`, and **say the value was missing.** Offer to backfill it rather than inferring quietly |

**`invalidated` is the one to be firm about**, because it is the value most likely
to look prunable. Old, no successor, nothing points at it — every mechanical
signal says go, and the field is the only thing saying the project has an open
question here.

## 4. Read each one before proposing it

**A record's age is not evidence about its contents.** Everything so far has been
mechanical and none of it has read a word of the reasoning.

Per candidate, know and be able to say:

- **What was decided**, in a sentence
- **What replaced it**, or that nothing did
- **Why it stopped being the answer** — beyond the enum value
- **What in the project still reflects it**, if anything

**A record you cannot summarise is one you have not read**, and it does not get
proposed.

## 5. Check nothing still points at it

```sh
grep -rn "ADR-0004" --include="*.md" --include="*.toml" .
```

Three kinds of pointer, and all three disqualify:

| | |
| --- | --- |
| **`superseded_by` from another record** | The successor explains itself by reference to this. Deleting it leaves a dangling redirect and a position with no visible history |
| **A body wikilink** — *"for why we moved off this, see …"* | Same problem, less visibly |
| **A citation from anywhere else** — a README, a type definition, a `CLAUDE.md` | Something outside the record set depends on this reasoning being findable |

**A pointer is a fact, not an obstacle to route around.** Rewriting the citation
so the record becomes deletable is the same act as deleting a cited record, with a
step in between.

## 6. Propose one at a time; never batch

**One record, one decision, one confirmation.** No *delete all eligible*, no
select-many list, no summary table offering a yes at the bottom.

**Because batching is the whole failure mode.** Twelve records approved in one
keystroke is not twelve decisions — it is one decision about a number, made by
somebody who read at most the first two. The awkwardness is the feature.

For each, put the step 4 summary in front of them with what step 5 found, and name
the options: **delete**, **keep**, or **keep and say why** — that last one is worth
offering, because a record somebody deliberately kept during a prune is one nobody
should propose again.

**An agent never decides this.** Not in any mode, not with prior blanket approval,
not because the last eleven were approved. The proposal is the agent's; the
deletion is theirs.

## 7. Delete in its own commit

**One commit for the prune, holding what the records said.** The reasoning is
about to stop being in the working tree, and `git log` is where somebody will come
looking.

```
Prune 2 decision records archived past retention

Retention is 3y (.luma/config/decision-records.toml). Both were archived
in 2021, are cited nowhere, and are not the target of any superseded_by.

- ADR-0004 Vendor the catalog per project (decided 2020-06-02,
  archived 2021-11-30, retired). Each project kept its own copy of the
  catalog. Ended when bundles became the unit of distribution and the
  copy had nothing left to hold.

- ADR-0011 Two config formats side by side (decided 2021-01-18,
  archived 2021-09-04, retired). TOML for projects, YAML for
  machine-local. Ended when the machine-local side moved to TOML too.

Approved by: human:fsmith, record by record.
The agent proposed; it did not decide.

Recoverable: git show <this-commit>^:<path>
```

**Summarise each record in the message.** A commit saying *pruned two records* has
moved the reasoning somewhere nobody will find it — the summary is what makes
`git log --grep` a usable index of what a project used to believe.

**Name the person and say the agent did not decide.** A deletion attributed to
whoever ran the tool reads, years later, as something that happened rather than
something somebody chose.

## 8. Report what stayed, not only what went

```markdown
**Deleted** — 2

| ADR | Title | Decided | Archived | Reason |
|---|---|---|---|---|
| 0004 | <title> | 2020-06-02 | 2021-11-30 | retired |
| 0011 | <title> | 2021-01-18 | 2021-09-04 | retired |

**Kept**

| ADR | Archived | Reason | Why it stayed |
|---|---|---|---|
| 0007 | 2021-02-11 | superseded | `superseded_by` target of ADR-0019 |
| 0009 | 2022-08-01 | retired | Cited from `docs/SPEC.md` |
| 0012 | 2021-06-30 | **invalidated** | Marks an open gap — never proposed |
| 0013 | — | — | No `archived` date, no `archived_reason`. Backfill offered |
| 0016 | 2020-04-19 | retired | Kept on request: "the reasoning still comes up" |

`archived/` 14 · eligible 6 · deleted 2 · missing metadata 1
```

**The *Kept* table is the more useful half**, and the reason to run this workflow
even when the answer is nothing. It is the only artefact that says *these were
looked at and they earned their place*, which is what stops the same six records
being re-examined every year.

**`Kept on request` should stay kept.** Where the bundle later grows a way to
record that on the record itself, this is the field it wants.
