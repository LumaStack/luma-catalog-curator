---
type: policy
title: What each luma tool does
description: The tools, the one job each performs, and when to use them. Read before installing or invoking any of them.
applies_to:
  - command: luma-foreman
  - command: luma-catalog-curator
  - topic: choosing which luma tool does a job
---

# What each luma tool does

**Three activities, and they are the whole map.** Every question of the form
*which tool do I use* resolves by asking which of these you are doing.

| activity | who does it | tool |
| --- | --- | --- |
| **adopt knowledge into a project, and keep it working** | everyone | **`foreman`** |
| **tend a catalog you publish** | the few who publish one | **`luma-catalog-curator`** |
| **build the tools themselves** | their maintainers | ordinary development; no luma tool |

**Most people only ever need the first row.** A catalog is an endgame rather
than a starting requirement — content earns its way up from a project, and most
adopters never publish anything.

## The tools

| | one job | state |
| --- | --- | --- |
| **`luma-foreman`** | adopts bundles into a repository and projects them at agents | **working** |
| **`luma-clarify`** | resolves ambiguity in written requirements | working |
| **`luma-backlog`** | keeps a project's intended work | working |
| **`luma-catalog-curator`** | checks a catalog for what only a catalog can see, and reports what it costs | **working** |
| **`luma-leader`** | not a tool. A place an organization keeps what outlives one project | n/a |

**`luma-leader` and `luma-foreman` are role metaphors and the rest are not**,
which is deliberate rather than untidy. Names of tools added from 2026-08-23
onward say the verb they perform.

## Engines are installed; not forked. Everything else is yours

**That single line is what tells a tool from content**, and it settles most
questions about what you may change.

| | | may you fork it |
| --- | --- | --- |
| **engines** | `foreman`, `clarify`, `backlog`, `catalog-curator` | **no.** Upgrade them; do not diverge |
| **content** | catalogs, bundles, your headquarters, your projects | **yes. All of it is yours** |

**An adopted bundle is content and is still not yours to edit in place.** It is
a vendored copy: editing it means the next adoption silently discards your
change, and nobody upstream ever learns somebody wanted it. Fork it into your
own namespace instead, or send the change to the catalog it came from.

## Where a tool writes

**Two homes, and the rule of thumb is committed versus yours.**

```
.luma/                 committed. What this project declares
~/.config/luma/        yours. Machine-local, never committed
```

**The reverse of each is the failure that matters.** Committed-but-personal is
somebody's private business in a shared repository. Uncommitted-but-inside
`.luma/` means two people on two machines read different rules for the same
project, which is a correctness failure in the one system whose job is saying
what the rules are.

**Anything under `.claude/`, `CLAUDE.md` or `AGENTS.md` is generated and
disposable.** Regenerate it rather than editing it. Where a tool writes into a
file you also write, it owns a region marked `luma:begin` and `luma:end` and
touches nothing outside it.

## You are not a different kind of user when you maintain the tools

**Working on a luma tool does not make you a special class of adopter**, and
believing otherwise produces tooling with a privileged path nobody else can
test. A maintainer runs `foreman` against a tool repository exactly as anybody
runs it against theirs.

What maintainers additionally need is context about the estate — its layout,
its release process, its conventions — and that is a **separate bundle**
(`luma/luma-maintainers`) rather than a mode of this one. **The two are
additive.** Adopt both in a repository that builds the tools; adopt only this
one everywhere else.
