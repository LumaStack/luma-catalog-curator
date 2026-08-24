---
type: type_definition
defines: decision_log
---

# Decision log

One document holding many decisions, newest first. What a project keeps before
a directory of separate records is worth the overhead.

**It declares no fields of its own.** Everything it needs — `title`,
`description`, `modified` — arrives from the root type, and per-decision
metadata cannot live in frontmatter here because there is more than one decision
in the file. Each entry carries its own *Settled* date in the body instead.

The type earns its place on its name alone: it tells a reader and a tool that
this file contains *many* decisions rather than one, which is the difference
that decides how to parse it and what a link to it means.

## Why this exists at all

A directory of records is the better long-term shape, and a project with three
decisions does not have a long term yet. One file is cheaper to write, and more
usefully, it is one thing to point an agent at — *read this and you know what
has been decided here* — where a directory means listing and reading *n* files
to answer the same question.

That advantage shrinks as the file grows and disappears once anything generates
an index (§11), so treat this as the starting shape rather than a choice
between equals.

## Graduating

When the file becomes unwieldy, split it: one `decision` document per entry,
under `.luma/records/decisions/`. [[migrate-decisions]] is that job — it settles
the numbering in one pass, reconstructs what supersedes what from prose that
recorded it as an edit, and repoints everything that cited the file before
removing it.

"Unwieldy" is deliberately a judgment. A rule that fails a project for keeping
twenty decisions in one file is a rule people route around, so a tool should
report the size and let someone decide.

**The split is not reversible in practice.** Individual records accumulate their
own `created`, `modified` and `verified` events once they exist separately, and
collapsing them back into one document discards all of it. Graduate when the
file is genuinely painful, not in anticipation.
