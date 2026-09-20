---
type: bundle
type_version: "0.0.1"
title: lumastack/luma-catalog/luma-tools
version: 0.13.0
published: 2026-09-19
stage: draft
consumers: [project, organization]
description: Using the luma tools — which one does what, getting them onto a machine, standing a project up, and the get-then-apply loop that puts knowledge in front of an agent.
---

# Luma tools

**How to use the tools, for people who did not write them.** Everything here is
about consuming: installing an engine, adopting bundles into a repository, and
making an agent aware of what was adopted.

**It carries no knowledge about building the tools.** That is
`lumastack/luma-catalog/luma-maintainers`, and the two are additive rather than alternatives — a
repository that builds a tool adopts both, everywhere else adopts only this.

## What is here

**Policy**

- [[what-each-tool-does]] — the three activities, which tool answers which, and
  the engines-versus-content rule. Read first.

**Procedures**

- [[adopt-knowledge]] — the loop that matters: get, apply, verify.
- [[install-the-tools]] — getting an engine onto a machine and wired up.
- [[initialize-luma]] — standing `.luma/` up in a repository that has none.
- [[migrate-into-luma]] — moving an existing project's scattered material in.

## Loading

Two documents are `mandatory` and that is one more than usual. [[adopt-knowledge]]
earns it because **the failure it prevents is silent**: a project that takes a
bundle and never applies it looks correct from every angle and reaches no agent
at all. An
adopter who never reads that procedure finds out months later, or not at all.

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

`0.10.3` — **the manifest declares `lifecycle: draft`.** The field was absent, and
absent reads as `unknown` — *nobody has said*. Something was known: this is
developed by its maintainers for their own use, and its shape can reverse
without notice.

**Publication did not promote it.** Being reachable by somebody who did not
write it makes the question live rather than answering it, and the answer here
is *still a draft* — which is a legitimate thing to publish, and says more than
silence did.

Patch: a fact written down. Nothing an adopter is obliged to do has changed, and
`unknown` promised nothing that `draft` withdraws.

`0.10.2` — **references to the knowledge format name sections instead of numbering them.** The format removed section numbers, so every `§n` here pointed at a position that no longer exists — and a stale number resolves to the wrong section rather than to nothing, which is why none of them were reported. Decorative citations are dropped; the rest name what they meant.

Patch: wording only. No rule, field or procedure changed.

`0.10.1` — **`entry_point` is now `entrypoint`.** One word, so the same word names the same thing at every level it appears.

Patch: one key renamed. Same value, same meaning, same `optional` presence, and `luma-foreman` reads both spellings while the rename lands.

`0.10.0` — **`initialize-luma` and `migrate-into-luma` arrive from
`luma-layout`.** Both are tool operations: one is now little more than *run
`luma-foreman init`*, and the other is a procedure somebody performs with the
tools in hand.

**The cut is by verb.** `luma-layout` says *where things go*; this bundle says
*how to run the tools that put them there*. A bundle whose job needs two verbs
is usually two bundles, and standing a directory up was the second verb over
there.

**Where the layout is concerned, this bundle points rather than restates.** The
directory's tiers, the committed-only invariant, and how to resolve a configured
location are `luma-directory-layout`'s in the `luma-layout` bundle. Nothing here
requires it to be adopted — the paths these workflows use are the defaults, and
the reference is depth.

**What an adopter has to do:** nothing, unless you adopted `luma-layout` only for
these two workflows, in which case adopt this instead.

`0.9.2` — **bundle IDs in this catalog gained their namespace.** A bundle here
is `lumastack/luma-catalog/<name>` rather than `luma/<name>`, because the
namespace now derives from where the catalog lives instead of being declared.
Every reference in this bundle's prose is updated.

**A fork can no longer publish under this catalog's name.** It lives somewhere
else, so it is named something else, and its bundles sit beside these in a
project rather than colliding with them.

*Type names are unaffected.* `type: luma/catalog` and its siblings name the
format, not this catalog, and resolve separately.

Patch: nothing but the identifiers a reference points at.

`0.9.1` — **the description named two commands that no longer exist.** It
called this the *adopt-then-project loop*; both words were renamed in 0.9.0 and
the description was missed. It is now the *get-then-apply loop*.

That line is the one an adopter reads first — it is what `catalog show` prints
and what a browser would index — so it was the worst remaining place for it.
*Projected* is also gone from `adopt-knowledge`, where foreman now reports the
same state as `unapplied`.

Patch: no instruction changed. Every command in this bundle already said `get`
and `apply`.

`0.9.0` — **the foreman commands were renamed.** `adopt` is now `get` and
`outfit` is now `apply`. Every command in this bundle is written the new way.

**The old names are a hard error, not an alias.** `luma-foreman adopt` prints
`unknown command: adopt (renamed to: get)` and exits 1. Aliasing them would have
let this bundle keep working while still being wrong, which is exactly the
pressure that gets text like this corrected.

Breaking, which below 1.0 the minor position carries: following this text needs
`luma-foreman` at or past the rename. An older engine rejects every command
here, and the error names the replacement rather than leaving you guessing.

`0.8.0` — **what to do when a generated file conflicts.** Two branches that
both adopted something will both have rewritten `CLAUDE.md`, the skills and
`routing.toml`. Resolving that by hand produces a file that is wrong in a way
nothing reports, and the next `outfit` discards it — so the answer is always to
re-run the tool rather than to merge its output.

Minor: an adopter following the old text was not told what to do at the one
moment it matters.

`0.7.0` — **`applies_to` is now `matches`.** The old name obliged an author to
write a false sentence: `applies_to: everything` claims a rule governs
everything, and none does — what a rule governs is stated in its body, where no
frontmatter value reaches. The field says what makes a Document *surface*, which
is smaller and true, and it reads as a sentence in every form it takes: matches
`git commit`, matches always, matches nothing.

**The default reverses with it.** A Document that says nothing is now available
on request rather than loaded into every session. Nothing here is affected —
every rule in this bundle already states what surfaces it — but a rule that
genuinely should always be present now says `matches: always` rather than
staying silent and being treated as though it had.

Minor. Nothing a reader is obliged to do has changed; the field it is declared
in has been renamed, and `applies_to` is still read while the rename finishes.

`0.6.0` — **vocabulary.** `moment` becomes `event` — a moment is a point in
time and `applies_to` takes nouns. `compliance` is dropped wherever it was
saying nothing: a policy binds unless it says otherwise, so only a strong
default declares `recommended`, and a workflow's steps bind by being steps.
Type Definitions use `field_presence: required` for what was
`obligation: mandatory`, matching the format.

Minor. Nothing a reader is obliged to do has changed; what declares it has.

`0.5.0` — **`preload` is replaced by `compliance` and `applies_to`.** An author
now says how strongly a rule binds and when it governs; *when it is delivered* is
computed from those and never declared. Every rule here could state when it
applies, so **nothing in this bundle is loaded unconditionally any more** — it
arrives when the work matches and costs nothing before then.

Minor: a consumer reading `preload` finds nothing, and the loading behaviour of
every document changes.

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
