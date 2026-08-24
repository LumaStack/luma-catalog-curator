---
type: workflow
title: Record a decision
description: Find or establish where this project keeps decisions, then write one. Use when a position is settled, when an irreversible change is proposed, or when asked where decisions live.
preload: mandatory
---

# Record a decision

## Before anything: if you are looking for a decision, not writing one

**Load [[find-decision]] whenever any of these happens:**

- a link or citation to a decision does not resolve
- you have an `ADR-NNNN` and cannot find the file
- you are about to conclude that something **was never decided**

**That last trigger is the one that matters.** A record that has moved into
`archived/` is invisible to anybody looking only in `decisions/`, and the cost of
missing it is not a dead link — it is deciding something afresh that already had
an answer, with no supersession and no sign anybody had been there before.

**The number survives every move.** Same `ADR-NNNN`, same decision, wherever the
file is now — so a broken link is a lookup problem rather than a lost record.
[[find-decision]] has the search order and what to do with what it turns up.

## 1. Find where decisions live

Look in this order and take the first that exists:

1. `.luma/records/decisions/` — a namespaced directory of individual records
2. `.records/decisions/` — a generic directory of individual records
3. `docs/DECISIONS.md`
4. `DECISIONS.md`

`.luma/records/decisions/` wins when several exist, because it is the mature shape
and `DECISIONS.md` is what a project keeps before it needs a mature approach.

**If more than one exists, say so before doing anything else.** That is not a
preference to resolve quietly — decisions are in two places and no reader can
tell which is authoritative. Report it, and offer to consolidate into the
directory.

## 2. If none exists, ask

Do not pick for them. Present both options and what each costs:

> **A file** — `DECISIONS.md`, newest first. One thing to read start to finish
> and one thing to point an agent at. Best while there are only a handful of
> decisions.
>
> **A directory** — `.luma/records/decisions/`, one record per decision. Each gets
> its own history and can be linked to individually. Better once decisions
> accumulate, and the shape you will end up in eventually.

A project past brainstorming should generally take the directory. A project on
day one generally should not.

## 3. Write the record

**In a directory**, the filename is `ADR-NNNN-<slug>.md` — four digits, zero
padded, next unused number:

```
.luma/records/decisions/ADR-0007-catalog-not-registry.md
```

Two things to know about the numbering. It is sequential, so two branches can
both claim `ADR-0012` and someone has to renumber on merge — the cost of the
convention, accepted because a short handle to cite in conversation is worth
it. And the number is not the identity: the Document ID is the whole path, so
renumbering breaks inbound links exactly as any rename does.

**In a file**, append a section at the top rather than the bottom. Newest first,
so the most relevant thing is not at the end of a growing document.

Either way, the content is the same, and it is `type: decision` — see that type
for what a record carries and how status maps onto `lifecycle_status`.

## 4. Decide whether this is even a decision

Record a decision when a position is **settled**, not while it is being argued.
The test: could someone act differently tomorrow because of this? If not, it is
a note.

Record one **before** an irreversible or expensive change, not after. A record
written afterwards documents what happened; one written first is a decision.

## 5. Correcting and superseding

Do not silently edit a settled record.

- The **record** was wrong — a bad rationale, a claim that does not hold?
  Correct it in place, dated and visible.
- The **decision** changed? Write a new record, archive the old one, and point
  `superseded_by` at the replacement.

The second is the one people get wrong by reaching for the first, and the cost
is that the reasoning which produced the original position disappears.

**The test between them: would somebody who followed the old text now be in
breach?** If no, correct it — the record got better at saying what it always
said. If yes, the position moved and it needs a new number, however small the
edit looks. **A decision is never reversed under the number it was decided
under**, because that number is cited in places no edit can reach.

**When the test fails, say so and say why** — quote both texts, name who would
newly be in breach, and **lead with what is not being refused**: they can have
the change, today; only the number is unavailable. Then draft the superseding
record rather than leaving them with a task.

**A silent no teaches people the tool is broken**, and a refusal nobody explains
is also a refusal nobody can push back on — which is how a rule that is drawn in
slightly the wrong place stays there. [[decision-guidelines]] has the full
shape, including what to do when the same refusal keeps recurring.

## 6. Archiving moves the file

A record that is no longer the answer goes into `archived/`, beneath the
decisions directory:

```
.luma/records/decisions/
    ADR-0007-catalog-not-registry.md
    archived/
        ADR-0004-vendor-the-catalog-per-project.md
```

Four things happen together, and doing one without the others is the common
mistake:

1. `lifecycle_status: archived`, and `superseded_by` where something replaced it
2. `archived: YYYY-MM-DD` — the date it stopped being the answer
3. `archived_reason` — `superseded`, `retired`, `invalidated` or `noise`
4. The file moves

**Take a moment over `archived_reason`.** It is the field that tells a later
reader whether `archived/` holds finished business or an open gap — `invalidated`
means the project used to have an answer here and no longer does. See
`_types/decision` for what each value means and for the two things that look like
values and are not.

**The directory is what saves the context.** Nothing loads `archived/` by
default and a glob over `decisions/*.md` skips it, so what a reader opens is only
what still holds. That is the honest answer to *these records are getting
expensive* — a loading problem rather than a reason to delete anything.

**A move breaks inbound links**, because a Document ID is the whole path.
Repoint them in the same commit.

**Assume you will miss one.** A `CLAUDE.md`, a commit template, a document nobody
thought to grep — repointing is best-effort, and the record is still findable by
number when it fails. That is [[find-decision]]'s job, and it is the reason
archiving is safe rather than merely tidy.

**Deleting an archived record is a separate, deliberate act** —
[[prune-archived-decisions]], which only reaches `archived/` and only past a
retention period the project has set. Nothing about archiving implies it.

## 7. Graduating from a file to a directory

When the file is genuinely painful rather than merely long, that is its own
workflow — [[migrate-decisions]]. It splits the entries, reconstructs what
supersedes what, repoints everything that cited the file, and only then removes
it.

**Do not do it by hand from this workflow.** The mechanics look simple and the
two things that go wrong are not visible while you are doing them: the numbering
has to be settled in one pass before anything is written, and every citation of
the old file breaks silently the moment it is deleted.

**It is effectively one-way.** Once records exist separately they accumulate
their own `modified` and `verified` events, and collapsing them back discards
all of it.
