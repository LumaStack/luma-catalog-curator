---
type: bundle
version: 0.2.0
published: 2026-08-23
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

`0.2.0` — the catalog tool has a name: **`curator`**. It still does not exist.

Minor rather than patch because a reader who correctly understood `0.1.0` would
now say something different: the table said *unnamed*, so there was nothing to
call it. Naming it changes what somebody writes and asks for.

`0.1.0`. Written the day adoption and projection first worked end to end, from
one estate's practice with no outside adopter. Two things in it are known to be
provisional: **`curator` is named and does not exist**, so the table in
[[what-each-tool-does]] lists a tool nobody can install yet — deliberately, so
that the gap is visible rather than absent; and **no tool has a release or a
tag**, so installation tracks `main` and nothing can be pinned.
