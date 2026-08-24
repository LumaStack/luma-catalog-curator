---
type: type_definition
defines: decision
fields:
  decided:
    obligation: mandatory
    field_type: date
    desc: "when the decision was settled — not when the document was created"
  reopen_trigger:
    obligation: recommended
    field_type: text
    desc: "what would have to become true for this to be worth revisiting"
  superseded_by:
    obligation: optional
    field_type: wikilink
    desc: "the decision that replaced this one — quoted (§8); set together with lifecycle_status: archived"
  archived:
    obligation: recommended
    field_type: date
    desc: "when this stopped being the answer. Set together with lifecycle_status: archived; the clock a retention period measures from"
  archived_reason:
    obligation: recommended
    field_type: enum
    values: [superseded, retired, invalidated, noise]
    desc: "why it stopped being the answer. Set together with lifecycle_status: archived"
---

# Decision

One settled position and the reasoning that settled it. One file per decision.

Follows the [Architecture Decision Record](https://adr.github.io/) conventions
even where the decision is not architectural — the shape holds for any decision
worth keeping, and borrowing an established convention costs nothing.

## The fields it does not declare

`lifecycle_status`, `created`, `modified` and `verified` all arrive from the
root type, and between them they cover what an ADR calls *status*:

| ADR status | here |
| --- | --- |
| proposed | `lifecycle_status: draft` or `provisional` |
| accepted | `lifecycle_status: stable` |
| superseded | `lifecycle_status: archived` plus `superseded_by` |
| retired | `lifecycle_status: archived`, no `superseded_by` |
| **rejected** | **no distinct expression — see below** |

Supersession is a **relationship, not a status** — §6 of the specification says
so directly — which is why `superseded_by` is a wikilink rather than a state.
That makes the successor reachable from the document a reader actually lands on.

`lifecycle_status` also governs **what you may edit**, not only how settled the
decision is. That ladder is in [[decision-guidelines]].

## Open: rejected has nowhere to live

**A decision that was considered and never adopted cannot be distinguished from
one that was adopted and later withdrawn.** Both are `archived`, and the only
difference is prose.

That gap matters more than it looks. **A rejected decision is the one that most
prevents re-litigation** — it is the record that answers *we thought about that
and here is why we did not*, which is exactly the question that returns every
few months. Filing it identically to something that was once in force loses the
distinction a reader needs first.

Three ways out, none chosen:

- A `rejected` value on `lifecycle_status`, which is a change to the format's
  core rather than to this type.
- A field on `decision` alone — cheap, and it means a general question gets a
  local answer that nothing else can reuse.
- `archived` with the rejection stated in the body. No new mechanism, and lossy:
  nothing can find rejected decisions without reading them.

Recorded rather than solved, because the right answer depends on whether other
document types need the same distinction — and none exist yet to ask.

## `decided` is not `created`

A decision can be drafted for a week and settled in a meeting. `created` records
when the file appeared; `decided` records when the position became binding. They
are frequently different and only one of them is the fact people cite.

## `archived` is when it stopped, and it is a third date

`decided` says when a position became binding and says nothing about when it
ceased to be. A decision settled in 2019 and retired last month was in force for
six years, and no combination of the other fields can tell you that.

**Set it whenever you set `lifecycle_status: archived`**, whether or not there is
a `superseded_by`. It costs one line at the moment the information is in front of
you and is unrecoverable a year later, when the best available answer is whichever
commit happened to touch the file.

**It is the clock a retention period measures from.** [[prune-archived-decisions]]
reads it and nothing else, and a record without it is not eligible — which is the
practical reason to write it, and also the reason not to backdate one generously
to make a record eligible.

**Archiving usually also moves the file**, into `archived/` beneath the decisions
directory, so the records a reader loads are only the ones still in force. That is
a convention of this bundle rather than something the format defines; the field is
what carries the fact, and the directory is what saves the context.

## `archived_reason` — why it stopped, in four values

`lifecycle_status: archived` says a record is no longer the answer and nothing
says why. That distinction is the one a reader needs first, and it is the one
`archived` alone cannot carry.

| | |
| --- | --- |
| `superseded` | **A different decision replaced it.** Pairs with `superseded_by`; the successor is the answer now |
| `retired` | **It reached its planned end.** A re-open trigger fired, a stopgap expired, the thing it governed is gone. Nothing replaced it and nothing needs to |
| `invalidated` | **The reasoning stopped holding**, and nothing has replaced it yet. An assumption proved false, a constraint disappeared. **This one marks a gap** |
| `noise` | **It was never a decision.** Filed as one during brainstorming, no position in it. Archived rather than deleted, because deleting is not what this bundle does |

**`retired` and `invalidated` look alike and are the pair worth separating.** Both
end with no successor, and only one of them leaves the project undecided about
something it used to have an answer for. **`invalidated` is a to-do**; `retired`
is finished business. A reader scanning `archived/` for what needs re-deciding is
asking exactly this question, and nothing else in the record answers it.

**`superseded` is partly redundant, deliberately.** `superseded_by` already
implies it. Keeping the value means the four cases are readable from one field
without cross-checking another, and a `superseded` with no `superseded_by` is a
cheap consistency check rather than a silent hole.

### What looks like a value and is not

**A record that rotted is corrected, not archived.** Dead links, renamed
terminology, an example that stopped being true — the *decision* still holds and
the *record* got stale. Routing that to archival throws away a position that is
still in force.

**And correcting rot must never change the decision underneath it.** Fixing the
prose is licence over the prose only: clarify, refine, strengthen the argument,
tighten wording that could be read two ways — but a record that comes out of a
correction saying something different from what it said going in is a reversal
wearing a cleanup's clothes, and it needs a new ADR with `superseded_by`. The
operative test is below, in *Correcting versus superseding*: **would somebody who
followed the old text now be in breach?**

Where the rot is bad enough that the reasoning genuinely no longer holds, the
record is not corrected at all — it is `invalidated`, and the project has an open
question rather than a tidier document.

**Saving context is not a reason.** Every archival saves context — it is the
benefit of the mechanism, true of all four values equally, so as a value it would
carry no information at all. *This is expensive to keep loading* is the reason to
archive **something**; `archived_reason` records which something, and *why this
one*.

### Open: who directed it is a second axis, and has no home

**"Archived on a directive from the architecture board" is real and is not a
reason** — it is an authority. It can co-occur with any of the four values, which
is what makes it a separate axis rather than a fifth entry.

Three ways out, none chosen:

- **`modified.by: team:architecture-board`.** Free, uses the existing actor
  grammar, and wrong in the common case: `modified.by` records who edited the
  file, which is usually not who directed it.
- **A second field** — `archived_by_directive`, an `actor`. Honest and cheap, and
  it is a field invented before anything reads the first one.
- **Prose in the body.** No mechanism, and nothing can find directed archivals
  without reading every record.

**Recorded rather than solved, because the routing that would consume it does not
exist yet.** The four values above answer *is this a gap, and is there a successor*
— which is what a policy sweep asks first. Authority becomes worth a field when
something needs to treat a directed archival differently from a local one, and
until then it is a guess about a consumer nobody has built.

## What a record contains

The frontmatter is the smaller half. The body carries the argument, and the
sections below are the working shape rather than a mandated template:

- **What was decided**, stated first and plainly.
- **Why it matters** — what breaks if this is got wrong.
- **How to apply it** — what someone does differently now.
- **Deferred alternatives**, each with a re-open trigger. A path not taken is
  **deferred, never rejected**: recording it as rejected discards the reasoning
  and invites the same argument again from scratch.
- **Standing consequences** — what this now forbids or requires elsewhere.

## Correcting versus superseding

The distinction that matters most in practice, because getting it wrong destroys
either the record or the reasoning. [[decision-guidelines]] covers what each
`lifecycle_status` permits; this is the field mechanics.

**Correct in place when the *record* was wrong** — a mistaken rationale, a claim
that does not hold, an example that was never true. The decision still stands;
what was written about it did not. Leave the correction visible and dated.

### Correcting never changes the decision. Only how it is explained

**This is the rule the whole numbering scheme rests on.** An ADR number is a
promise that the position under it never moved — it is cited in commits, in
conversation, and from other records, and every one of those citations is wrong
the moment the same number means something different.

| A correction may | A correction may never |
| --- | --- |
| clarify wording that could be read two ways | **reverse the position** |
| tighten loose phrasing so it cannot be misread | widen or narrow what it applies to |
| add reasoning that was always the reason and went unwritten | turn a preference into a requirement, or the reverse |
| fix dead links, renamed terminology, an example that stopped being true | change the answer and keep the number |
| strengthen the argument for the same position | soften a position because it became inconvenient |

**The test: would somebody who followed the old text now be in breach?**

If no, it is a correction — the record got better at saying what it always said.
If yes, the position moved, and it needs a new record with `superseded_by`
pointing at it, however small the change looks in the diff.

**That test is what separates stricter *wording* from a stricter *decision*.**
Editing *"prefer TOML"* into *"always TOML"* is not a clarification: everybody
who chose YAML under the old text was compliant and is not any more. Editing
*"use TOML"* into *"use TOML — this includes machine-local settings, which was
always intended"* is a clarification, because nobody's existing conduct changed
status.

**Reversal under the same number is the failure this prevents**, and it does not
announce itself. It arrives as a sequence of reasonable edits — a hedge added, a
scope trimmed, an exception carved out — until the record says the opposite of
what it said, with no archived predecessor and nothing in the history a reader
would think to look for. **A superseded decision is visible. A quietly rewritten
one is not**, which is why the heavier mechanism is the one that protects the
record.

**Supersede when the *decision* changed.** Write a new record, set the old one's
`lifecycle_status: archived` and point `superseded_by` at the replacement:

```yaml
lifecycle_status: archived
superseded_by: "[[ADR-0012-catalogs-do-not-inherit]]"
```

**Quote it.** `[[…]]` is YAML flow-sequence syntax, so an unquoted wikilink
parses as a nested array rather than a string and no parser complains — the
record stays valid and the redirect simply never resolves. §8 of the
specification carries the warning; this is the field in this bundle most likely
to meet it.

The old reasoning stays readable, which is what lets someone see why the
position moved rather than only that it did.

ADR convention says an accepted decision is immutable and everything is a
supersession. That is right for reversals and heavy for errata — a typo in the
rationale does not warrant a new record and a redirect.
