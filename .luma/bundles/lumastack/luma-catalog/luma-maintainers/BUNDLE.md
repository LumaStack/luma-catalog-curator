---
type: bundle
type_version: "0.0.1"
title: lumastack/luma-catalog/luma-maintainers
version: 0.14.0
published: 2026-09-19
stage: draft
consumers: [project, organization]
description: Working on the luma tools themselves — the repositories and the boundary each defends, publishing to the universal catalog, and changing a type without making every tool upgrade at once.
---

# Luma maintainers

**For repositories that build the luma tools**, and nowhere else. It carries the
estate's own layout, its release and publication practice, and the migration
discipline that keeps six repositories from having to move together.

**Adopt it only in a repository that is part of the estate.** Everything here is
noise in a project that merely uses the tools — foreman's release process is not
information an Acme developer needs, and a bundle that ships it to them has
mistaken *important to us* for *useful to them*.

## It is additive to `lumastack/luma-catalog/luma-tools`, never a replacement

**A maintainer is also a consumer**, and that is the reason these are two
bundles rather than two modes. Building foreman does not exempt you from using
it — the tools get run against the tool repositories exactly as anybody runs
them against theirs.

So a repository in the estate adopts **both**. Nothing here contradicts anything
there, and if it ever does, one of the two is wrong rather than the split.

**The separation is by repository, not by person.** You are not a different kind
of user when you maintain the tools; you are a user standing in a different
repository.

## What is here

**Policy**

- [[the-estate]] — six repositories, the boundary each defends, and where a new
  thing goes. Read first.

**Procedures**

- [[publish-to-the-catalog]] — promoting a bundle, and getting the version
  honest.
- [[change-a-shared-type]] — expand, migrate, contract, and why it is never one
  release.

## Loading

Only [[the-estate]] is `mandatory`. Both procedures are `optional` — you load the
one you are doing.

**The boundaries are the mandatory part because crossing one is silent.**
Nothing errors when a distribution concern lands in the format or a check lands
in the catalog; it simply becomes true, and it is expensive to unwind once
something depends on it.

## Consumers

`project` and `organization`, because **the estate is mostly projects.** Building
foreman, the format or the curator happens in a repository, and
[[publish-to-the-catalog]] and [[change-a-shared-type]] are things you do
standing in one. A headquarters needs [[the-estate]] as well, so both values are
right and neither alone is.

**The narrower value this field used to carry was answering the wrong question.**
`consumers` says *would this bundle function in a repository like yours* — a
floor. What this bundle wants to say is *this is ours rather than yours*, which
is a fence, and no field expresses one. Reaching for `consumers` made the
manifest contradict the body directly above.

**Until a fence exists, the restriction is prose**, and it is stated plainly at
the top: adopt this only in a repository that is part of the estate.

## Version

`0.11.3` — **the manifest declares `lifecycle: draft`.** The field was absent, and
absent reads as `unknown` — *nobody has said*. Something was known: this is
developed by its maintainers for their own use, and its shape can reverse
without notice.

**Publication did not promote it.** Being reachable by somebody who did not
write it makes the question live rather than answering it, and the answer here
is *still a draft* — which is a legitimate thing to publish, and says more than
silence did.

Patch: a fact written down. Nothing an adopter is obliged to do has changed, and
`unknown` promised nothing that `draft` withdraws.

`0.11.2` — **references to the knowledge format name sections instead of numbering them.** The format removed section numbers, so every `§n` here pointed at a position that no longer exists — and a stale number resolves to the wrong section rather than to nothing, which is why none of them were reported. Decorative citations are dropped; the rest name what they meant.

Patch: wording only. No rule, field or procedure changed.

`0.11.1` — **`entry_point` is now `entrypoint`.** One word, so the same word names the same thing at every level it appears.

Patch: one key renamed. Same value, same meaning, same `optional` presence, and `luma-foreman` reads both spellings while the rename lands.

`0.11.0` — **`consumers` was `organization` only, and the manifest contradicted
the body.** The body tells estate repositories to adopt this, and says the
separation is *"by repository, not by person — you are a user standing in a
different repository."* Those repositories are projects. `luma-foreman` had
adopted it, correctly by the body and against the frontmatter, and nothing
reported the mismatch because nothing can: **no repository declares what kind of
consumer it is**, so `consumers` is currently unenforceable from either side.

**The old value was carrying a restriction the field cannot express** — see
`## Consumers` above. The restriction itself is unchanged and still applies.

Minor: project repositories may now adopt what the body already told them to
adopt. Nobody doing nothing has to act.

`0.10.3` — **bundle IDs in this catalog gained their namespace.** A bundle here
is `lumastack/luma-catalog/<name>` rather than `luma/<name>`, because the
namespace now derives from where the catalog lives instead of being declared.
Every reference in this bundle's prose is updated.

**A fork can no longer publish under this catalog's name.** It lives somewhere
else, so it is named something else, and its bundles sit beside these in a
project rather than colliding with them.

*Type names are unaffected.* `type: luma/catalog` and its siblings name the
format, not this catalog, and resolve separately.

Patch: nothing but the identifiers a reference points at.

`0.10.2` — **`the-estate` described foreman as "adoption, projection,
inspection."** Two of those three are no longer words the tool uses. It now
says *getting, applying, inspecting*, which are the commands.

Patch: one cell of one table. The `## Version` history below still says
*projection* and is left alone — it records what was true when written.

`0.10.1` — **`adopt` is now `get` and `outfit` is now `apply`**, where
`the-estate` and `publish-to-the-catalog` mention them in passing.

Patch: neither sentence tells anybody to run anything. The `## Version` history
below is left as written — it records what was true at the time.

`0.10.0` — **`the-estate` cited a field that never existed.** It described the
adopter's missing selection as *the same question `preload_default` answers for
adopted bundles*. `preload_default` is not in the specification and never was: it
is an unbuilt idea from a `luma-leader` design draft, cited in a published policy
as though it had shipped. The gap is now described directly rather than by
reference to a mechanism a reader cannot go and read.

**And the bundle count was stale** — seventeen, where the catalog publishes
nineteen.

Minor. Two factual corrections; no rule changed.

`0.9.0` — **`applies_to` is now `matches`.** The old name obliged an author to
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

`0.8.0` — **vocabulary.** `moment` becomes `event` — a moment is a point in
time and `applies_to` takes nouns. `compliance` is dropped wherever it was
saying nothing: a policy binds unless it says otherwise, so only a strong
default declares `recommended`, and a workflow's steps bind by being steps.
Type Definitions use `field_presence: required` for what was
`obligation: mandatory`, matching the format.

Minor. Nothing a reader is obliged to do has changed; what declares it has.

`0.7.0` — **`preload` is replaced by `compliance` and `applies_to`.** An author
now says how strongly a rule binds and when it governs; *when it is delivered* is
computed from those and never declared. Every rule here could state when it
applies, so **nothing in this bundle is loaded unconditionally any more** — it
arrives when the work matches and costs nothing before then.

Minor: a consumer reading `preload` finds nothing, and the loading behaviour of
every document changes.

`0.6.0` — **the manifest is `BUNDLE.md`.** Reserved markdown files are now
ALL CAPS across the estate, because nobody types all caps by accident: a file
becomes load-bearing only when somebody deliberately made it so, and writing
`bundle.md` now fails in the safe direction — ignored rather than silently wired
into machinery. Minor rather than patch, and pre-1.0 that is the tier for a
breaking change: anything naming the old path by hand stops resolving.

`0.5.1` — *standard* becomes *policy*. Wording only: `policy` is the document
type the format defines and the word this estate uses everywhere else, and
`standard` was deliberately freed for the organization level rather than left
doing double duty.

Patch because a reader who correctly understood `0.5.0` behaves identically.
The subject noun changed; nothing it requires, permits or forbids did.

`0.5.0` — a repository does not vendor its own bundles into itself.

**Written after this catalog did exactly that.** It adopted two of its own
bundles, producing byte-identical duplicates in one repository, which
contradicts *reference within a repository, vendor across them*. The section
states the rule and is honest about what it costs: a catalog gets no projection,
because projecting what a repository *publishes* needs a selection mechanism
that does not exist yet.

`0.4.0` — **publication is an event.** Merging to `luma-catalog`'s `main` is
it, a required pre-merge job runs the checks, and a red run blocks the merge.
[[publish-to-the-catalog]] says that instead of naming a command and admitting
nothing runs it, and step 6 is renamed from *merge, then let adopters find it*
to *merge — which is publication*.

Minor rather than patch: a reader who correctly understood `0.3.0` believed the
consistency check was theirs to remember. They would now expect the job to
refuse the merge, and would read a red run as a defect in their change rather
than a broken pipeline.

**It also adds a check they have to satisfy**: `curator check --against` refuses
a bundle whose files moved while its version stood still. That is step 2's rule,
which this bundle already stated, made mechanical for the one part of it that is
mechanical. The tier stays the author's judgement — nothing here decides that.

**What has not changed:** no tag, no release, no notification. Adopters still
find a newer version by running `adopt` again and nothing tells them to. And
the enforcement is `luma-catalog`'s configuration rather than a property of the
tools — anybody else's catalog is unwired until they copy the job.

`0.3.0` — [[publish-to-the-catalog]] runs a command rather than describing one a
person has to do by hand. `luma-catalog-curator` exists.

**The honest part is what it still says afterwards.** The check is built and
wired to nothing, because publication is not an event — so the workflow now
names the command *and* says that nothing runs it unless somebody does.

`0.2.0` — the tool that checks a catalog is **`curator`**, named on 2026-08-23
by firing a re-open trigger while renaming was still free. Same reasoning as
`lumastack/luma-catalog/luma-tools` `0.2.0`: naming a thing the previous version called unnamed
changes what a reader writes.

`0.1.0`. Extracted from one estate's practice on the day adoption first worked,
which is real practice and not much of it.

**Two things in it are known to be incomplete.** There is no workflow for cutting
a tool release, because **no tool has a release** — installation is a clone and
a symlink, nothing is tagged, and writing the procedure before the capability
would be describing something that does not happen. And the catalog's own
consistency check is named in [[publish-to-the-catalog]] as a thing a person
names a command instead of a person, but nothing runs it: publication is still
not an event, so the check is available rather than enforced.
