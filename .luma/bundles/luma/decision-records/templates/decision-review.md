# Decision review template

**This one is a message, not a file.** Every other template here shapes something
written to disk; this shapes what gets put in front of a person when a decision
needs a call — during [[migrate-decisions]] in `together` or `reviewed` mode.

**It exists because the shape drifts.** Run without one, the same reviewer
presents entry 1 and entry 18 differently, and the person reviewing has to relearn
where the recommendation is every time. Consistency is worth more than elegance
here: they are reading twenty of these in a row.

## The blocks

```markdown
**<N-1> → ADR-<NNNN>, <lifecycle_status>.**

## <N> of <total> — <title>

**The entry, verbatim:**

> <the entry exactly as written, including its own hedges and typos>

**What you need to judge it:**

- <whether anything cites it, and from where>
- <whether a later entry amends or reverses it>
- <what has changed since it was settled>

**My recommendation — `ADR-<NNNN>`, `<lifecycle_status>`:**

​```yaml
type: decision
title: <title>
decided: <from the entry's Settled line, or recovered>
lifecycle_status: <draft|provisional|stable|archived>
reopen_trigger: <as written, or absent>
created:  { by: <original author>, at: <when it was written> }
modified: { by: <migrating actor>, at: <now> }
​```

<One or two sentences. Which rule decided the status, and where the date came from.>

**Supersession:** <none · supersedes ADR-NNNN · superseded by ADR-NNNN, so this
lands in `archived/` with `archived_reason: superseded`>

**Your decision:** <the actual options, named>
```

**Where the recommendation is `archived`**, the frontmatter block carries
`archived`, `archived_reason` and `superseded_by` too, and the sentence beneath it
says which of the four reasons and why — `retired` and `invalidated` look alike
and only one of them leaves the project with an open question.

## Why each block is there

**The lead-in line** reports the previous entry in one line, carried here rather
than sent as its own turn — correction latency is the same either way, and a
separate turn costs a round trip.

**Verbatim, always.** Paraphrasing a decision during review is how it quietly
becomes a different decision. Their hedges stay: *"we may regret this"* is part of
the record.

**"What you need to judge it" is the block that earns the review.** Anyone can
propose a status; the value is telling them what they would otherwise have to go
and look up — that three documents cite this entry, that entry 6 reverses it, that
the constraint it rests on disappeared in March.

**Show the frontmatter, not a description of it.** They can read
`lifecycle_status: provisional` faster than a sentence proposing it. It also means
the post-write report can be one line, because they have already seen it.

**The supersession line is never omitted**, including when the answer is `none`.
It is the field most likely to be wrong and least likely to be noticed, and a
blank where it should say `none` reads as *not checked* — which, often enough, it
was.

**Name the options in "your decision".** *Accept, change the status, split it, or
mark it superseded by 9* beats *what do you think?* — the second makes them invent
the choices.

## What not to do

**Do not write anything before they answer.** The recommendation and the record
are two turns. This template ends at a question for a reason.

**Do not offer deleting it.** There is no such option in this workflow — a spent
decision goes to `archived/`. See [[prune-archived-decisions]], which is a
different job on a different day.

**Do not restate the frontmatter after writing.** They read it here.

**Do not stack reviews.** One entry, one decision. Batching belongs in `reviewed`
mode, which has its own shape — a table of title, settled date, and proposed
number.
