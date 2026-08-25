---
type: bundle
version: 0.4.0
published: 2026-08-25
consumers: [project, organization]
entry_point: workflows/adopt-knowledge
description: Using the luma tools — which one does what, getting them onto a machine, and the adopt-then-project loop that puts knowledge in front of an agent.
---

# Luma tools

**How to use the tools, for people who did not write them.** Everything here is
about consuming: installing an engine, adopting bundles into a repository, and
making an agent aware of what was adopted.

**It carries no knowledge about building the tools.** That is
`luma/luma-maintainers`, and the two are additive rather than alternatives — a
repository that builds a tool adopts both, everywhere else adopts only this.

## What is here

**Policy**

- [[what-each-tool-does]] — the three activities, which tool answers which, and
  the engines-versus-content rule. Read first.

**Workflows**

- [[adopt-knowledge]] — the loop that matters: adopt, project, verify.
- [[install-the-tools]] — getting an engine onto a machine and wired up.

## Loading

Two documents are `mandatory` and that is one more than usual. [[adopt-knowledge]]
earns it because **the failure it prevents is silent**: a project that adopts and
never projects looks correct from every angle and reaches no agent at all. An
adopter who never reads that workflow finds out months later, or not at all.

[[install-the-tools]] is `optional` deliberately, though it is the first thing
chronologically. It is run once per machine, and machine setup is not something
a session working in a repository should be carrying.

## Consumers

Both levels. An organization's headquarters is a repository, adopts bundles, and
runs the same tools against itself.

## Why this exists as a bundle rather than a README

**Because a README is read by a person once and a bundle is loaded by an agent
every time.** The tools are used almost entirely through agents, and *how to use
foreman* was reachable only by somebody who thought to open the repository —
which is the same gap adoption exists to close, left open in the one place it is
most embarrassing.

## Version

`0.4.0` — **the manifest is `BUNDLE.md`.** Reserved markdown files are now
ALL CAPS across the estate, because nobody types all caps by accident: a file
becomes load-bearing only when somebody deliberately made it so, and writing
`bundle.md` now fails in the safe direction — ignored rather than silently wired
into machinery. Minor rather than patch, and pre-1.0 that is the tier for a
breaking change: anything naming the old path by hand stops resolving.

`0.3.1` — wording in [[what-each-tool-does]]: a tighter description, a shorter
heading, and a clause about renaming conventions cut as rationale nobody needed
at that point.

Patch because no normative sentence moved. A reader who correctly understood
`0.3.0` behaves identically — which is the test, and it is the tier most easily
got wrong for prose. Benjamin's wording.

`0.3.0` — **`luma-catalog-curator` exists.** Built the same day it was named, so
`0.2.0` was accurate for a few hours.

It also corrects the name `0.2.0` guessed at. That version wrote `luma-curator`
in the tool table while the repository became `luma-catalog-curator` — the
qualifier was added deliberately, to recover the guessability `curator` gave up
when it beat `cataloger`. **A bundle naming a command nobody can install is
worse than one admitting it does not exist yet**, so this is the correction that
mattered most.

`0.2.0` — the catalog tool has a name: **`curator`**. It still does not exist.

Minor rather than patch because a reader who correctly understood `0.1.0` would
now say something different: the table said *unnamed*, so there was nothing to
call it. Naming it changes what somebody writes and asks for.

`0.1.0`. Written the day adoption and projection first worked end to end, from
one estate's practice with no outside adopter. Two things in it are known to be
provisional: **no tool has a release or a tag**, so installation tracks `main`
and nothing can be pinned — which is now owed to three tools rather than two.
And **`luma-catalog-curator` is built but wired to nothing**: publication is not
an event, so its checks run when somebody remembers.
