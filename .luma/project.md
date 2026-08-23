---
type: luma/project
title: luma-catalog-curator
disclosure_level: public
description: The command-line tool that runs where a catalog is written — consistency checks over a set of bundles, and the report of what a catalog is becoming. Open it for anything done to a catalog, never for anything done to a project.
owns:
  - checks whose subject is a set of bundles rather than one bundle
  - checks comparing a catalog against its own history, which only a publisher has
  - the report of what a catalog costs an adopter
  - reading a catalog manifest, including the YAML subset that requires
must_not_own:
  - adoption, vendoring, or anything done to a project repository
  - checks whose subject is a single bundle in isolation
  - any organization's conventions about how a bundle should be written
  - what a standard says, or the reasoning behind it
---

## Why it exists

**A catalog can be internally contradictory in ways no individual project could
ever detect.** A bundle both mandated and deprecated. A starter pinning a
version the same catalog's own mandate forbids, which would make every new
consumer born failing. A requirement tagged with a word no consumer can declare,
so it never fires and everything reports green.

**Those are caught where the only person who can fix them is standing.** Letting
one through means it surfaces in front of an adopter who owns neither bundle and
whose only recourse is forking.

## Boundaries

**It runs where a catalog is written; foreman runs where bundles are adopted.**
That is a difference in runtime location, which is the rule this estate splits
projects on. Different repositories, different people, different cadences.

**It never adopts.** A curator that also adopted would have collapsed the split
it exists to express.

**It never decides obligations.** Whether a bundle is mandatory is the catalog
author's declaration. This checks that the declarations are mutually
satisfiable; it has no view on what they should say.

**It contains no knowledge of any particular catalog.** The test is mechanical:
a check that only makes sense for `luma/` is a bug. A tool that compiled an
organization's conventions in would be deciding standards rather than checking
them, and useless to the second organization that ran it.

**It checks sets, not artifacts.** A dangling link inside one bundle is
foreman's to report — those checks exist, and duplicating them here is the
overlap that stays unextracted until the shape is known.

## Status

Early, and honest about two gaps. **Publication is not an event**, so every
check designed to run "at publication" is a job somebody has to wire up and
nothing enforces that they did. **Nothing has dependencies**, so roughly half
the designed checks have nothing to check and are absent rather than stubbed.

Python 3.11+, standard library only. The full design is in
`luma-leader/docs/curator.md`.
