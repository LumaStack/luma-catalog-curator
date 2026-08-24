---
type: workflow
title: Find a decision
description: Locate a decision record from a number, a title, or a link that no longer resolves. Use whenever a citation points at nothing, or before concluding that something was never decided.
---

# Find a decision

**A broken link to a decision is almost never a missing decision.** It is a stale
path — the record moved, most often into `archived/`, and something that pointed
at it did not get updated.

## The number is the identity for finding

**The ADR number survives every move.** `ADR-0007` is `ADR-0007` in
`decisions/`, in `archived/`, in a subdirectory somebody invented, and in a commit
from two years ago. **Same number, same decision, wherever the file is now.**

**That is not a contradiction of "the number is not the identity."**
[[record-decision]] says the Document ID is the whole path, and it is right — for
*linking*. A wikilink resolves against a path, so a move breaks it. The two
statements answer different questions:

| | |
| --- | --- |
| **the path** | what a link resolves against. Breaks when the file moves |
| **the number** | what a human or agent searches by. Survives the move |

So a dead link is a lookup problem, not a lost record, and the number is what you
look up with.

## 1. Search by number, everywhere before concluding anything

```sh
git ls-files "*ADR-0007*"                    # tracked, anywhere in the repo
find . -name "ADR-0007-*.md" -not -path "./.git/*"
```

**One command covers the whole repository**, which is the point — do not check
`decisions/`, find nothing, and stop. The overwhelmingly likely answer is
`archived/`, and it is the one place a reader who knows only the live directory
will never look.

**Where the citation gives a title rather than a number**, search the text:

```sh
grep -rl "catalogs do not inherit" --include="*.md" .
```

Citations by title are common — a record cited as
`[DECISIONS.md](docs/DECISIONS.md) — *The PDF extractor is pypdfium2*` has no
number in it at all — and the title usually survives the move as well as the
number does.

## 2. If it is not in the tree, look in history — for the *last* version

**History holds every version of a record, and only the last one is the
decision.** Records get corrected in place — that is what
[[decision-guidelines]] permits and expects — so an early commit may carry the
mistaken rationale that a later correction fixed, wording that was ambiguous
enough to need tightening, or a dead reference somebody repaired.

**Recovering an old version resurrects a corrected error**, and it arrives
looking exactly as authoritative as the version that replaced it. There is
nothing in the text to say it was superseded by an edit.

**So take the newest commit that touched it, always.** `git log` is
newest-first, so the first result is the one you want — `head -1`, never
`tail -1`. And **say which commit you read it from**, so the next person can
check whether you took the last one.

**Three things it could be, and a different command finds each.**

**It was deleted.** Find the most recent commit that removed it, and read the
parent — **which is the last version by construction**, and the reason this is the
cleanest of the three:

```sh
git log --diff-filter=D --format="%H %ad %s" --date=short -- "*ADR-0007*" | head -1
git show <sha>^:.luma/records/decisions/archived/ADR-0007-<slug>.md
```

Take the first line, not the last. A record deleted, restored and deleted again
has two matches, and the older one predates whatever the restoration changed.

The commit message is worth reading before the record —
[[prune-archived-decisions]] requires a summary and a named approver, so it should
say who removed it and why.

**It was renamed or moved so long ago that the current name is unrecognisable.**
`--follow` traces it across renames:

```sh
git log --follow --name-status --format="%H %ad" --date=short -- "*ADR-0007*" | head -20
```

The newest entry names where it ended up; the older ones are how it got there.

**It never was a separate file.** A project that has not run
[[migrate-decisions]] keeps its decisions in one `DECISIONS.md`, and one that has
run it has a history where they used to live there:

```sh
git log --all --format="%H %ad" --date=short -- "*DECISIONS.md" | head -1
git show <sha>:docs/DECISIONS.md          # its final state, not an early draft
```

**The last commit that touched the file is the version to read**, and for a
migrated project that is the version [[migrate-decisions]] left behind — markers
against every entry and the breakdown table at the top, which together say where
each decision went. That is a better answer than the record itself: it tells you
the new number.

Use `git log -S "ADR-0007" --oneline` to find *when* something entered or left the
file, but read the content from the newest commit rather than from the one the
search happened to surface.

**A number in an old commit or conversation may not mean what it means now.**
Numbering is sequential, so two branches can both claim `ADR-0012` and somebody
renumbers on merge — [[record-decision]] names this as the accepted cost of a
short handle. **Check the title matches**, not just the number, whenever the
citation is older than the last renumbering you know about.

## 3. Read what you found before acting on it

**Finding an archived decision and following it is the failure this workflow can
cause**, and it is worse than not finding it at all. You went looking because you
wanted the current answer, and `archived/` holds the ones that are not.

Check three fields before using anything from `archived/`:

| | |
| --- | --- |
| `lifecycle_status: archived` | **this is not the answer.** Whatever the reasoning says |
| `superseded_by` | **follow it.** The record it points at is the answer, and this one exists to explain why the answer moved |
| `archived_reason` | `superseded` → follow the link · `retired` → finished, nothing replaced it · `invalidated` → **the project has an open question here** · `noise` → it was never a decision |

**`invalidated` is the one that changes what you do next.** It means the project
used to have an answer and no longer does — so the thing you came looking for is
not merely elsewhere, it is undecided, and that is worth saying to whoever asked.

**Something recovered from git history is not in force either**, whatever it says.
Say where it came from — *found in the commit that deleted it, 2024* — so nobody
downstream mistakes an artefact for a live position.

## 4. Fix the link you came in through

**Otherwise the next person runs this whole procedure again.** You have the answer
in front of you and it costs one line.

**Relinking during archival is best-effort and this is where it shows.** Moving a
record into `archived/` is supposed to repoint everything citing it, and in
practice a citation gets missed — in a `CLAUDE.md`, in a commit template, in a
document nobody grepped. **A dead link found is evidence of a missed relink**, not
just an inconvenience.

**So check whether it is one link or many:**

```sh
grep -rn "ADR-0007" --include="*.md" --include="*.toml" .
```

If several point at the old path, fix them together and say so. One stale link is
an oversight; six is an archival that half happened, and leaving five for somebody
else to trip over is the same decision made five more times.

## 5. When it genuinely is not there, say that plainly

**"I could not find it" and "it was never decided" are different findings, and
only one of them is safe to act on.**

Absence of a record is not evidence that nothing was decided. It may have been
decided in a conversation nobody wrote down, in another repository, or in a file
this search did not cover. **Concluding *no decision exists* and then deciding it
afresh is how a project quietly reverses itself** — the new position is filed with
no supersession, no archived predecessor, and no sign that anybody ever thought
about it before.

Report what you searched — the tree, history, deleted files, the old
`DECISIONS.md` — so the next person starts where you stopped rather than
repeating it. **Then ask** before treating the question as open.
