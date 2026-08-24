---
type: bundle
version: 0.2.1
published: 2026-08-22
consumers: [project, organization]
entry_point: workflows/record-decision
description: Decisions recorded with their reasoning, deferred alternatives, and re-open triggers. Spent decisions are archived rather than deleted.
---

# Decision records

A decision without its reasoning is not finished. The answer is perishable — it
gets superseded, or the constraint that forced it disappears — but the argument
is what survives, and it is the only thing that lets someone six months later
tell a decision that still holds from one that was never revisited.

This bundle carries the contract for a decision record, the workflow for keeping
them, and the rule for when to correct one versus supersede it.

It applies at both levels deliberately. An organization records decisions about
how it works; a project records decisions about how it is built. The documents
are the same shape, and which level a given adopter wants is not the
publisher's call to make.

## One of the `*-records` family

Named for the artifact it produces in the `.luma/records/` tier, alongside
whatever else comes to live there — `audit-records`, `log-records`,
`incident-records`.

The suffix names the **kind** of thing: every one of them produces records, and
each prefix says which. It also keeps the noun convention every other bundle
follows, and leaves the imperative form free for the workflow inside — the
bundle is `decision-records`, the workflow is [[record-decision]], and neither
shadows the other.

*The cost, stated once:* they do not sort together in a listing. A `record-*`
prefix would have grouped them, at the price of every bundle in the family
reading like a workflow.

## What is here

**Workflows**

- [[record-decision]] — where records live, what to do when nothing exists yet,
  and how archiving moves a spent record into `archived/`.
- [[find-decision]] — locating a record from a number, a title, or a link that
  no longer resolves, including recovering the last version from history.
- [[migrate-decisions]] — split an existing `DECISIONS.md` into individual
  records, once. Reconstructs supersession and repoints everything that cited
  the file.
- [[prune-archived-decisions]] — the only workflow here that deletes anything. It
  reaches `archived/` and nothing else, past a retention period the project sets.

**Policy** — [[decision-guidelines]]: when to record one, what makes it survive,
and what you may edit once it is settled.

**Templates** — [a record](templates/decision-template.md) ·
[a decision review](templates/decision-review.md)

**Types**

- `_types/decision` — a single decision record.
- `_types/decision_log` — one document holding many decisions, for projects
  small enough that a directory would be overhead.

## Archived, not deleted

**A decision that stops being the answer moves to `archived/` beneath the
decisions directory.** It keeps its file, its history and its inbound links, and
stops being loaded.

**That exists to answer the one honest argument for deleting records: context.** A
directory where six of forty still hold is expensive to read and impossible to
skim, and that is a loading problem rather than a reason to destroy reasoning.
Nothing globs into `archived/`, so the fix costs a directory.

**Deleting is possible, separate, and awkward on purpose.**
[[prune-archived-decisions]] cannot see a live record, will not run without a
committed retention period, and takes one record at a time with a person
confirming each. A workflow that offered pruning as a step would teach that
pruning is a normal part of keeping records — and a project whose decisions can be
deleted routinely is one whose decisions nobody trusts, because an absent record
stops meaning anything in particular.

## Loading

Only [[record-decision]] is `preload: mandatory` — a consumer that cannot load
it should fail rather than proceed without it, because everything else here is a
contract it refers to.

**[[decision-guidelines]] is `recommended`.** It is the craft rather than the
mechanism: what makes a record survive, and what you may edit once it is settled.
A consumer that cannot load it can still write a well-formed record, so failing
the session would be too strong — but it should say it proceeded without it,
because the record it produces will be formally correct and probably worse.

**The other three workflows are `optional` on purpose**, for two different
reasons.

[[migrate-decisions]] and [[prune-archived-decisions]] are jobs somebody starts
deliberately, once or rarely, and neither has anything to say to an agent that is
not doing them. Loading a migration procedure into every session because the
project might one day run one is the cost `preload` exists to avoid.

**[[find-decision]] is `optional` for a subtler reason, and it is the case worth
understanding.** It fires reactively — nobody sets out to run it — so the
straightforward move is to preload it. The cheaper one is to preload a *pointer*:
[[record-decision]] is already `mandatory`, and it opens by naming the three
triggers that should cause this one to be loaded.

**That is progressive disclosure working, and it has one failure mode.** It holds
only while the trigger is in context. An agent that does not know a search
procedure exists does not go looking for one — it hits a dead link, concludes
nothing was ever decided, and re-decides it. **So the pointer is load-bearing in a
way the procedure is not**, and anything that trims [[record-decision]] should
leave those three lines alone.

The Type Definitions carry no `preload` at all, which means `optional`: they are
read when something needs to know what a field means, not held in context
against the possibility. That is the field working as intended rather than an
omission.

## Version

`0.2.1` — a heading no longer says how many things are beneath it. Wording only.

Patch: no normative sentence moved and a reader who correctly understood
`0.2.0` behaves identically. See `writing-style` in `luma/project-documentation`
for the rule and the failure it prevents.

`0.2.0` — archiving as a real mechanism, and the two workflows around it. New
content; existing use is unaffected except that an archived record now wants three
fields it did not before.

**It started as a pruning question and ended somewhere else.** Migrating a long
`DECISIONS.md` raises *can we drop the ones that are noise*, and the first answers
tried were gates — prune only retired decisions, only on early projects, only past
a retention period, warn loudly otherwise. Every version of that was a ladder of
judgement calls an agent would have to make correctly every time.

**The complaint underneath it was context, not storage.** A directory where six of
forty records still hold is expensive to read, and nobody was actually asking to
destroy reasoning. `archived/` answers that completely and costs a directory:
nothing globs into it, so what a reader loads is only what still holds.

**So deleting became a separate workflow that cannot reach a live record.**
[[prune-archived-decisions]] sees `archived/` and nothing else, refuses to run
without a committed retention period, and confirms one record at a time. The
awkwardness is deliberate — a workflow with a pruning *step* teaches that pruning
is a normal part of keeping records, and a project whose decisions can be deleted
routinely is one whose decisions nobody trusts. Once a few are gone, an absent
record could mean never written, dropped as noise, or removed by somebody it
embarrassed, and nothing distinguishes them.

**`archived_reason` came from asking what to record at the moment of archiving.**
The candidate list mixed three different questions, and separating them is most of
the value: *replaced*, *retired* and *rot* are about the decision; *directive from
leadership* is an authority; *saves tokens* is true of every archival and so
carries no information at all. What survived is one enum —
`superseded | retired | invalidated | noise` — whose real work is separating
`retired` from `invalidated`, because only one of those leaves the project
undecided about something it used to have an answer for. The authority axis is
recorded in `_types/decision` as an open question rather than guessed at.

**Correcting a record may never move the position, and that is now stated as a
test rather than an intention.** *Would somebody who followed the old text now be
in breach?* If no, it is a correction; if yes, it needs a new record, however
small the diff. The rule was implicit in *correcting versus superseding* and
implicit was not enough — the failure it prevents does not announce itself. A
reversal arrives as a sequence of reasonable edits, a hedge here and a trimmed
scope there, until the record says the opposite of what it said with no archived
predecessor and nothing a reader would think to look for. **An ADR number is a
promise the position never moved**, and it is cited in commits, in conversation
and from other records — none of which an edit can reach.

The test also settles the case that made the rule ambiguous: *stricter wording*
is a correction and a *stricter position* is not. `draft` is the one status
exempt, because nothing is binding and nothing is citing it yet.

**A rule that refuses without explaining is two failures, not one.** The person
is left thinking the tool is broken when it is working, and the rule loses the
only evidence that would tell it apart from a rule drawn in the wrong place. So a
failed test owes an explanation: both texts quoted, who would newly be in breach,
the superseding record drafted rather than left as somebody's task, and **the
rule named so it can be argued with**. It leads with what is *not* being refused,
which is almost everything — a decision may be reversed today; only reusing the
number is unavailable.

**Changing that rule is itself a decision**, with a record and a re-open trigger,
because it governs how every other record may change. The rule about not silently
changing decisions is not exempt from itself.

**[[find-decision]] exists because relinking is best-effort and archiving is
not.** Moving a record into `archived/` is supposed to repoint everything citing
it, and in practice something gets missed — a `CLAUDE.md`, a commit template, a
document nobody grepped. The recovery rests on one property: **the ADR number
survives every move**, so a dead link is a lookup problem rather than a lost
record.

That sits alongside [[record-decision]]'s *the number is not the identity*
without contradicting it. **The path is the identity for linking; the number is
the identity for finding.** A wikilink resolves against a path and breaks when
the file moves; a human or an agent searches by number and does not.

**Reading the wrong version is the hazard the history search introduces.**
Records are corrected in place, so an early commit can hold the mistaken
rationale a later correction fixed — and it arrives looking exactly as
authoritative as the version that replaced it. The rule is to take the newest
commit that touched the file, and to say which one it was.

**`decision-guidelines` drops from `mandatory` to `recommended`.** It had claimed
mandatory alongside the entry point, which overstated it: a consumer that cannot
load the craft can still write a well-formed record, and `mandatory` means *fail
rather than proceed*. Nothing else in the bundle changes — `recommended` still
says load it upfront whenever you can, and report when you did not.

**`migrate-decisions` restates rather than references `migrate-ideas`.** Bundles
never depend on one another, so the mode table, the denominator rule and the
propose-and-stop discipline are written out again here. Three things are genuinely
different and are not borrowed: ADR numbers must be assigned in one pass up front
because they are cited, supersession has to be reconstructed from a file that
recorded it as prose, and every inbound citation of the old file breaks silently
the moment it is deleted.

`0.1.0` rather than `1.0.0`. The conventions here are extracted from practice
rather than invented, but that practice is days old and has been run in one
place. `1.0.0` would claim more than is true.
