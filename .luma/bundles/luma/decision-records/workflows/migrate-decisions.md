---
type: workflow
title: Migrate a DECISIONS file
description: Split a single DECISIONS.md into individual records, reconstruct what supersedes what, repoint everything that linked to the file, and only then remove it. Use once per project that has one.
---

# Migrate a DECISIONS file

A one-off per project. Two things make it riskier than it looks, and neither is
the splitting.

**A decision file is cited.** Ideas are written and read once; decisions are
pointed at — from a README, from a type definition, from the CLAUDE.md that
tells an agent to read them before changing something. Splitting the file breaks
every one of those references at once, and a broken citation to a decision is
worse than a missing one, because the reader concludes the reasoning was never
recorded.

**The file flattened relationships that the records have to carry again.** In
one document, *this reversed that* is a paragraph. In a directory it is
`superseded_by`, and if nobody reconstructs it the archive reads as a set of
decisions that all still hold, several of which contradict each other.

Everything below serves those two, plus the rule shared with any migration:
**removing the original before anybody has checked** is the failure, so
verification is a step rather than a feeling.

## 1. Ask how involved they want to be

**Before reading anything**, because it changes how every step below is run.

| | |
| --- | --- |
| **delegated** | run the whole thing and record what happened. They read the result |
| **reviewed** | propose in batches — a table of title, settled date, and proposed number — take feedback, and repeat until they are ready to sign off |
| **together** | one decision at a time: show what is needed to judge it, recommend, and decide jointly |

**Show them that table. Do not ask an open question.** *How involved do you want
to be?* makes somebody invent options they have no way of knowing exist — and the
natural answer to it is *you decide*, which lands on `delegated`, the one mode
this step warns about.

**Unless they already named one.** *Mode: together* in the opening request is an
answer; re-presenting the table then is noise. **Confirm what it means in one
line** — *together, so one decision at a time, propose and stop, nothing written
until you say* — so they know what they opted into without being asked again.

**`together` and `reviewed` both present decisions one way** — see
[the decision review template](../templates/decision-review.md). Run without it
the shape drifts, and somebody reading twenty reviews in a row has to relearn
where the recommendation is each time.

**`delegated` still stops at step 10.** Deleting the original always needs their
confirmation, whichever mode is chosen.

**The mode governs who is asked. It never governs what is checked.** Every step
below runs identically in all three: the denominator and the numbering are
settled before writing begins, entries are taken in order with nothing deferred,
supersession is reconstructed rather than assumed absent, and every inbound
reference is repointed.

**Only an explicit decision advances a step.** A question, a request for more
detail, a correction to something unrelated, or agreement to a different point
is **not** signoff. Neither is silence, and neither is interest.

**Propose and stop.** The recommendation and the writing are two turns and never
one. An agent that recommends a status and writes the record in the same breath
has replaced their judgement with its own while appearing to collaborate.

## 2. Ask where the records go, and whether any leave this repository

Two questions, both asked once, up front. **Neither has a right answer that
holds across projects**, which is why they are asked rather than assumed.

### The destination is usually settled, so do not re-ask it

**A migration is a move to a directory. That much is the premise** — somebody
asking for this has already decided the file is not enough, and re-running the
file-versus-directory question from [[record-decision]] step 2 makes them decide
something they came here having decided.

Take the first that applies:

| | |
| --- | --- |
| `.luma/` exists | `.luma/records/decisions/`. **Do not ask** |
| `.records/` exists, no `.luma/` | `.records/decisions/` |
| neither | **ask** — and do not create `.luma/` to make room. Migrating decisions is not a reason to bring a directory structure into somebody's project |

**Say where they are going in one line, then move on.** Confirmation is cheap;
a question they have already answered is not.

### Whether a decision may leave this repository is theirs

**Ask, every time. Each situation is different**, and the wrong default is
damaging in both directions — routing decisions out of a repository that owned
them scatters the record, and refusing to route leaves decisions filed where
nobody affected by them will look.

Put the three postures in front of them:

| | |
| --- | --- |
| **stays put** | every decision becomes a record in this repository. No question asked per entry |
| **flag only** | everything stays, and anything that looks misfiled is named in the closing breakdown as a follow-up. Nothing moves during the migration |
| **route** | where an entry plainly belongs to another project, propose moving it, per entry |

**`route` is the expensive one, and say so when offering it.** It needs a list
of candidate destinations before entry one — the headquarters declaration where
there is one, the repository index it points at, sibling checkouts otherwise —
and it turns a mechanical split into a scoping exercise. Worth it when a file
has accumulated other projects' decisions; overhead when it has not.

**A decision is not an idea, and this is where they differ most.** An idea is a
want, and filing it in the wrong place costs it a reader. A decision is
**already binding on somebody**, and moving it changes who is bound — which is a
change to the decision, not to its filing.

**Recommend `flag only` when unsure.** It costs nothing during the run, loses
nothing, and turns the routing question into a list somebody can act on
deliberately rather than a series of judgement calls made while they were
thinking about something else.

## 3. Read the whole file first

### Settle the denominator before writing anything

**A heading is not necessarily a decision, and a sub-heading usually is not one
at all.** This is the opposite of the bias that applies to an ideas file, and
getting it backwards is the common failure here.

| shape | usually |
| --- | --- |
| `##` with `###` beneath it | **one decision.** The sub-headings are its reasoning — *why this*, *what it costs*, *how to apply it* — and splitting them produces four records that each say a quarter of something |
| `##` holding two independent choices | **two decisions.** [[decision-guidelines]] is explicit: bundled decisions cannot be superseded independently, so the first one to change drags the other with it |
| `##` naming a subject rather than a position | **probably not a decision.** See the triage below |

**Propose the split and get it confirmed before record one.** A denominator that
moves mid-run makes *3 of 20* meaningless, and it lands the question at the worst
moment — somebody deep in one decision now has to arbitrate the shape of the file.

### Then assign every number, before writing any record

**ADR numbers are settled in one pass, up front.** This has no analogue in any
other migration and it is not optional.

**Because the numbers are cited.** `ADR-0012` gets said out loud, written into a
commit message, and linked from another record. Renumbering afterwards breaks
inbound links exactly as any rename does — the number is a handle, and the
Document ID is the whole path.

**And because they are ordered by settled date, not by file position.** A
`DECISIONS.md` is newest-first, so the numbering runs **bottom to top**: the
oldest decision in the file becomes `ADR-0001`. You cannot assign that
incrementally while reading top-down, which is why the whole map is produced
before anything is written.

```sh
grep -n "^## \|^\*\*Settled" docs/DECISIONS.md    # headings and their dates, in file order
```

Three cases the map has to resolve:

- **Two settled the same day.** File order breaks the tie — lower in the file is
  older. Say which you took; it is arbitrary and should look arbitrary.
- **An entry with no settled date.** Recover it from history rather than
  guessing, and see below.
- **A record that supersedes another** gets the higher number, always. The
  numbering then reads in the direction the reasoning moved.

**Show them the map and get it agreed.** A table of number, title and settled
date, in the order the numbers will run. It is the last cheap moment to move one.

### Recover missing dates from history, and say when you could not

`decided` is mandatory on a `decision`, and an entry without a `**Settled …**`
line still has one — it is just not in the file.

```sh
git log -S "<the heading text>" --format="%ad  %an" --date=short --reverse \
  -- docs/DECISIONS.md | head -1        # the commit that introduced the entry
```

**That is when it was written down, which is a ceiling rather than the date.** A
decision settled in a meeting and recorded a week later gets the later date, and
history cannot tell you that. Present it as recovered, not as found.

**When nothing recovers it, ask.** They may simply remember. Where nobody does,
use the recording date and **say in the record that it is the recording date** —
a `decided` value silently off by a month is worse than one annotated as
approximate, because only one of them can be corrected later.

### Retired decisions go to `archived/`. This workflow does not delete any

**A migration is the moment somebody is most tempted to tidy**, so it is worth
saying plainly what this one does with a decision that is spent: it moves it, and
that is the only thing on offer.

```
.luma/records/decisions/
    ADR-0007-bundles-are-versioned.md
    ADR-0009-catalogs-do-not-inherit.md
    archived/
        ADR-0004-vendor-the-catalog-per-project.md
```

Superseded, retired, or a position nobody ever acted on — it becomes a record like
any other and lands in `archived/`.

#### It answers the only honest argument for deleting

**Context.** A directory of forty records where six still hold does cost
something: every one is a candidate to load, and a reader cannot tell live from
dead without opening it. That complaint is real, and **it is a loading problem
rather than an existence problem** — which is exactly what a subdirectory fixes.

Nothing loads `archived/` by default, a glob over `decisions/*.md` skips it, and
the directory somebody opens holds only positions that hold. The reasoning stays
greppable, linkable, and reachable from the record that replaced it.

**Two costs, stated honestly.** A record's Document ID is its whole path, so
archiving is a move and a move breaks inbound links — the same problem as step 6,
solved the same way. And `archived/` is a convention this bundle introduces rather
than something the format defines, so nothing enforces it.

**Which makes this migration the cheapest moment it will ever be.** Every inbound
reference is being rewritten in step 6 anyway, so archiving now costs one extra
path in a pass already happening. Archiving later is that whole pass again, for
one file.

#### Deleting is a different workflow, and nothing here reaches it

**This migration archives. It never deletes**, in any mode, with any
confirmation. There is no *Pruned* column, no prompt asking what to drop, and no
flag.

**Deleting exists** — [[prune-archived-decisions]] — and it is separate on
purpose. It only ever reaches `archived/`, so a live decision is not one step away
from it; it runs against a retention period the project has to have set
deliberately; and it takes them one at a time.

**None of that is available during a migration**, because a record archived five
minutes ago has not been archived for the retention period. **That ordering is the
design**: archive now, and if the project still wants the file gone in three
years, that is a different act on a different day by somebody who has read it.

**Why the separation is worth the friction.** A workflow with a pruning step
teaches that pruning is a normal part of keeping records, and a project where
decisions get deleted routinely is one whose decisions nobody trusts. The value of
a record is not that it exists — it is that its existence was never optional, so a
reader can conclude something from what is *not* there. Once deleting is routine,
an absent decision means *never recorded*, *removed as noise*, or *removed by
somebody who did not like it*, and nothing distinguishes them.

**The failure that matters most is the damning one.** A record that survives when
it is flattering and goes when it is inconvenient is not a record, and nobody sets
out to build that — it arrives one reasonable prune at a time, each with a good
argument.

**So when they ask to prune during this run, archive it, say the other workflow
exists, and move on.** Not a refusal and not a lecture — `archived/` gives them
what they actually wanted, which was the context back.

### Take them in order, and defer nothing

**File order — newest first, as the file is written.** The numbering already
runs the other way and that is fine; reviewing in file order keeps the reader
oriented in the document they know.

**Nothing is grouped and handled at the end.** Batching the awkward entries — the
ones that are not decisions, the supersession pairs, anything that resists the
shape — means those calls arrive when attention is lowest. **The awkward ones
need the most attention and would get the least.** It also breaks the only
progress signal there is: *nine of twenty* means nothing if four were quietly set
aside.

### Triage: is this entry even a decision?

For each, decide: *record it*, *fold it into another record*, or *it is not a
decision*. Two tests catch most of what should not become a record.

**A subject is not a decision.** *Naming*, *observability*, *testing* — a heading
that names a topic and then discusses it has not stated a position. Read the body
before ruling: often there is a real decision inside it wearing a topic's
heading, and the fix is a title in active voice rather than a prune. **Where
there genuinely is no position, it is a note** — say what it actually is and
where it would belong.

**Reasoning that supports a decision is not a second decision.** The longest
sections are usually one position with its argument attached, and splitting them
produces records that cannot stand alone. The test from [[decision-guidelines]]
holds: *could someone act differently tomorrow because of this?*

### The file will be messy, and that is normal

| Mess | Rule |
| --- | --- |
| **An entry amended in place** — *"Settled 2026-08-09. Renamed on 2026-08-21 — the trigger fired"* | **This is a supersession wearing an edit's clothes.** Step 4 |
| **Two entries where the later reverses the earlier** | Two records, `superseded_by` on the older. **Never merge them into one** — the superseded reasoning is what shows why the position moved |
| **An entry with no settled date** | Recover from history, say it was recovered. Never guess |
| **One entry holding two independent choices** | Notify and recommend a split. Do not perform one silently — the denominator and the numbering were agreed up front |
| **Cross-references between entries** — *"the same failure as splitting to manage context"* | Becomes a wikilink once both records exist. Collect them; resolve them in step 5 when the numbers are real |
| **An entry that is a note, a log, or an open question** | Do not force it into decision shape. Say what it is and where it belongs. A `ROADMAP` item recorded as a settled position is a decision nobody made |
| **An entry whose reasoning is missing** — the position with no *why* | Migrate it as it stands and say the reasoning is absent. **Never reconstruct one.** A plausible rationale is indistinguishable from the real one and will be believed |
| **A decision that is plainly wrong now** | Not this workflow's business. Migrate it, and raise superseding it as separate work afterwards |

**The rule underneath all of them: surface and help resolve — never resolve
alone.** Do the reading. Name which of two entries you think supersedes the
other and why. Say what an entry with no reasoning appears to rest on and how
confident that is. **An agent that flags a mess and stops has done half a job.**

**Then stop.** Migration preserves; it does not improve. Step 9 verifies it, but
by then an enlarged decision is already written.

## 4. Reconstruct what supersedes what

**The step with no counterpart in any other migration, and the one that decides
whether the archive is readable.**

A single file records change by editing. *We chose X. Amended: actually Y.* That
works in one document read top to bottom, and it does not survive the split —
each record is now read alone, by somebody who will never see the other one
unless it is linked.

Per entry, the call from [[decision-guidelines]], and **the test that decides it
is whether somebody who followed the old text would now be in breach.** If no, the
entry is one record with a correction in it. If yes, the position moved and it is
two records, however much the file made it look like an edit.

**The *record* was wrong — supersession is not involved.** A mistaken rationale,
a dead link, a claim that never held. One record, corrected, dated and visible.

**A migration is when this gets got wrong in the quiet direction.** Tidying an
entry into cleaner prose is the whole job here, and the same motion will happily
tighten *prefer* into *always* or drop a caveat that was load-bearing. That is not
a cleanup — it is a new decision filed under an old date with nothing archived and
no successor. **The wording may get better; the position may not move.**

**Where an entry needs a position moved, say so at its turn rather than doing
it.** Quote the two texts, name who would newly be in breach, and put the choice
in front of them: migrate it as written, or migrate it as written *and* write a
superseding record with today's date. **Both are available and neither is a
refusal** — what is unavailable is the third option, which is filing the new
position under the old entry's date and number as though it had always said that.

**The *decision* changed — two records.** The old position becomes its own
record, `lifecycle_status: archived`, with `superseded_by` pointing at the
replacement. The new position gets the higher number.

```yaml
lifecycle_status: archived
superseded_by: "[[ADR-0012-luma-hq-renamed-to-luma-leader]]"
```

**Quote it.** `[[…]]` is YAML flow-sequence syntax, so an unquoted wikilink
parses as a nested array and nothing complains — the record stays valid and the
redirect silently never resolves.

### The worked example, because this is where judgement is needed

An entry reading:

```markdown
## Naming

**Settled 2026-08-09. `luma-hq` renamed to `luma-leader` on 2026-08-21 —
the trigger fired.**

… the original naming argument …

### The rename, and the defect that forced it

… why the first name was wrong, and what replaced it …
```

**That is two decisions and one supersession**, and every signal says so: two
dates, a re-open trigger that fired, and a position that is no longer in force.
It becomes an archived record at the earlier `decided` date pointing at a
current record at the later one.

**The tempting wrong answer is one record with both dates in it**, because that
is what the file looked like. It loses the thing worth having — that a re-open
trigger was written, fired, and was honoured, which is the evidence the
convention works at all.

**The other wrong answer is dropping the superseded half** as merely historical.
It is the half that explains why the current name exists.

**Where it is genuinely unclear, ask.** Guessing toward supersession clutters the
directory with records; guessing away from it destroys history. Those are not
symmetric, but neither is cheap, and the person who wrote the entry usually
remembers in one line.

## 5. Write the records

The shape is [the record template](../templates/decision-template.md) and the
contract is `_types/decision`. Four things a migration decides differently.

**`decided` comes from the entry, never from today.** The `**Settled …**` line
first, history second, and annotated as approximate where it is neither.

**`created` and `modified` are not both the migration.** The reasoning was
written when it was written, by whoever wrote it — so `created` carries the
original date and author, and the **migration is a `modified` event**, which is
exactly what that field is for. Writing today's date and the migrating agent into
`created` claims authorship of somebody else's argument, and it is the one error
here worth avoiding outright.

```yaml
created:  { by: human:fsmith,      at: 2026-08-09T00:00:00Z }   # from the entry
modified: { by: agent:opus-5,      at: 2026-08-22T14:20:00Z }   # this migration
```

Where the original author is unrecoverable, `unknown:unknown` is honest and far
better than the name most likely to be right.

**`lifecycle_status` is decided, not defaulted — and it is the one field the
migration invents.** The file did not carry it. That sits in tension with
*migration preserves and does not improve*, and the resolution is that it is
**asked rather than assumed**, in every mode.

| | |
| --- | --- |
| `stable` | settled and being relied on. **It also freezes the record** — afterwards only the explanation may change, and only with agreement |
| `provisional` | in force, still on trial. Freely editable in place |
| `archived` | no longer the answer. Goes to `archived/`, and takes three more fields |

**Lean `provisional` where they have no view.** `stable` is a claim about how
settled something is *and* a lock on editing it, and taking that lock during a
mechanical move is how a typo becomes permanent.

**An `archived` record needs `archived`, `archived_reason`, and `superseded_by`
where there is a successor** — and this is the last moment any of them is cheap.
The file being migrated has the whole history in front of you; a year from now the
best available answer is whichever commit happened to touch it.

```yaml
lifecycle_status: archived
archived: 2026-08-21
archived_reason: superseded
superseded_by: "[[ADR-0012-luma-hq-renamed-to-luma-leader]]"
```

**`archived_reason` is the one worth pausing over**, and `invalidated` is the
value most often missed. `retired` is finished business; `invalidated` says the
project used to have an answer here and no longer does. A migration that files
every dead entry as `retired` has flattened away every open gap in the file — see
`_types/decision` for the four values.

**Resolve the cross-references now that the numbers are real.** The prose
references collected in step 3 become wikilinks, quoted in frontmatter and bare
in the body. A cross-reference left as *"see the decision about context above"*
points at nothing once *above* stops existing.

## 6. Repoint everything that pointed at the file

**The step most likely to be skipped and most damaging when it is**, because
nothing fails. The links simply stop resolving, and a citation to a decision
that 404s reads as reasoning that was never recorded.

```sh
grep -rn "DECISIONS" --include="*.md" --include="*.toml" . | grep -v "^./docs/DECISIONS.md:"
```

**Sweep beyond markdown.** A `CLAUDE.md` instructing agents to read the file
before changing anything, a README table of contents, a type definition citing a
decision by title, configuration naming the path.

Three shapes, and only the first is mechanical:

| | |
| --- | --- |
| **A bare link to the file** | Repoint at the directory |
| **A link citing a title** — `[DECISIONS.md](docs/DECISIONS.md) — *The PDF extractor is pypdfium2*` | Repoint at that record. **The citation names which one**, so this is exact rather than a guess |
| **Prose depending on the file existing** — *"read `docs/DECISIONS.md` first"* | Rewrite the sentence. A directory is read differently from a file, and a pointer that survives the link check can still be wrong |

**A missed reference is recoverable, and that is not licence to miss one.** Once
the records exist, the ADR number finds them wherever they end up —
[[find-decision]] is the procedure. What that buys is a floor rather than a
substitute: the reader who trips over the link still loses the time, and a
citation by title with no number is the case where recovery is hardest.

**Do this before the original is deleted, not after.** While the file is still
there, a missed reference is a stale link somebody notices. Once it is gone, it
is a dangling one that gives no clue what it pointed at.

## 7. Mark it migrated, in the original

Against each entry:

```markdown
> *Migrated to `.luma/records/decisions/ADR-0007-<slug>.md`.*
```

**Do not delete anything yet.** The marker is what makes verification possible,
and a half-finished migration with no markers is worse than one not started.

**Then say where it landed, in one line, carried into the next entry rather than
sent on its own.**

```
**11 → ADR-0004, provisional.**

## 12 of 20 — <title>
```

The frontmatter was proposed and agreed before anything was written, so
restating it is noise. **The exception is narrow:** anything in the record that
was not in the proposal gets a sentence — a supersession found, a date recovered,
a cross-reference resolved.

## 8. Report the breakdown

**Every fifteen decisions, and always when the file is finished** — whichever
comes first. End of file is the stronger trigger, because it is when somebody
decides whether to delete the original.

```markdown
**Migrated**

| # | ADR | Title | Settled | Landed | Modifications |
|---|---|---|---|---|---|
| 20 | 0001 | <title> | 2026-06-02 | `stable` | none |
| 14 | 0004 | <title> | 2026-07-11 | **`archived/`** | superseded by 0009 · date recovered |
| 9 | 0009 | <title> | 2026-08-09 | `provisional` | supersedes 0004 |
| 3 | 0016 | <title> | 2026-08-19 | `provisional` | split 1 of 2 |

**Not migrated** — nothing was deleted; these became no record at all

| # | Title | What it actually was | Where it belongs |
|---|---|---|---|
| 7 | <title> | an open question | `ROADMAP.md` |
| 12 | <title> | thinking-out-loud, no position in it | nowhere — said so, left in history |

**References repointed** — 14 across 6 files · 0 remaining

`.luma/records/decisions/` 14 · `archived/` 4 · not a decision 2
```

**`Modifications` is the column that earns the table.** Its vocabulary is
`none` · `retitled` · `date recovered` · `date approximate` · `split N of M` ·
`supersedes NNNN` · `superseded by NNNN` · `reasoning absent`. Scanning it
answers the only question worth asking in bulk: *did my decision survive as I
wrote it?*

**The reference line is not decoration.** It is the one number that says whether
step 6 was actually run, and `0 remaining` is the claim being made before the
original is deleted.

**Where the mode was `flag only`, the follow-up table goes here** — entries that
look like they belong to another project, named and not acted on.

### Write it into the original, not just the chat

**The breakdown goes at the top of `DECISIONS.md` before anything is deleted.**
Show it in the conversation too — that is what they respond to — but the file is
where it has to live.

**Because deletion is what makes it permanent.** Once the file is gone, its last
committed version is the only record, so that version should be the complete one.
A half-marked file frozen in history looks like a record and is not.

## 9. Verify before removing anything

**Both a person and an agent, if you can get both.** They miss different things:
an agent catches an entry with no marker and a link that no longer resolves, a
person catches a decision whose meaning did not survive the move.

- Every entry has a marker, or an explicit line saying it was not migrated
- Every named record exists, and every `superseded_by` resolves to one of them
- **No reference to the old file remains anywhere** — the grep from step 6,
  returning nothing
- Every `decided` traces to the entry or to history, and every approximate one
  says so
- Nothing acquired reasoning the original did not have
- **No position moved.** For each record, would somebody who followed the entry
  as written still be compliant with the record as written? A `no` anywhere means
  a decision was changed during a move, which is the failure this whole workflow
  is arranged to prevent

**That third one is the check with teeth.** The others fail visibly during the
run; a missed reference fails months later, to somebody who concludes the
decision was never recorded.

## 10. Archive, then delete on confirmation

**Archiving needs nobody's permission. Deleting needs the user's.**

The same rule as pruning, for the same reason: the original is somebody's work,
and a migration that ate it silently is the version of this that goes wrong.

Once confirmed, **delete the original.** Leaving it is the worst outcome — two
places holding the same decisions, drifting apart, with nothing saying which is
authoritative. That is precisely the split [[record-decision]] step 1 tells you
to report, created deliberately. The history keeps it.

**And it is effectively one-way.** Once records exist separately they accumulate
their own `modified` and `verified` events, and collapsing them back into one
file discards all of it. That is a reason to be sure, not a reason to hesitate:
the directory is the shape a project ends up in.
