---
type: bundle
version: 0.3.0
published: 2026-08-23
consumers: [organization]
entry_point: policy/the-estate
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

## It is additive to `luma/luma-tools`, never a replacement

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

**Workflows**

- [[publish-to-the-catalog]] — promoting a bundle, and getting the version
  honest.
- [[change-a-shared-type]] — expand, migrate, contract, and why it is never one
  release.

## Loading

Only [[the-estate]] is `mandatory`. Both workflows are `optional` — you load the
one you are doing.

**The boundaries are the mandatory part because crossing one is silent.**
Nothing errors when a distribution concern lands in the format or a check lands
in the catalog; it simply becomes true, and it is expensive to unwind once
something depends on it.

## Consumers

`organization` only, and deliberately narrower than most bundles here. There is
no sensible project-level reading of *how the luma estate is maintained* —
adopting it into a project would be adopting somebody else's internals.

## Version

`0.3.0` — [[publish-to-the-catalog]] runs a command rather than describing one a
person has to do by hand. `luma-catalog-curator` exists.

**The honest part is what it still says afterwards.** The check is built and
wired to nothing, because publication is not an event — so the workflow now
names the command *and* says that nothing runs it unless somebody does.

`0.2.0` — the tool that checks a catalog is **`curator`**, named on 2026-08-23
by firing a re-open trigger while renaming was still free. Same reasoning as
`luma/luma-tools` `0.2.0`: naming a thing the previous version called unnamed
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
