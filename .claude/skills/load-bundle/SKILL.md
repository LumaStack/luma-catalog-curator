---
name: load-bundle
description: Open one adopted bundle and see what it holds — its rules, what fires each one, and anything that applies throughout it. Use when a bundle's line looks relevant, or when asked to load a bundle by name.
---

<!-- luma-foreman:generated navigation. Regenerate with `luma-foreman apply`; edits are lost. -->

# Open a bundle

Read `.luma/bundles/<bundle-id>/INDEX.md`.

**The bundle ID carries its namespace** — `lumastack/luma-catalog/git-secrets`,
never `git-secrets`. Guessing at one is the only way this fails, so take it from
`.luma/bundles/INDEX.md`, which lists every bundle this project carries. Use `/list-bundles`
if you do not have a name at all.

**What you get: the bundle's own index**, shipped inside it and frozen at its
version — what it is for, what must be read before acting on anything in it,
every document with what surfaces it, and what is reachable only by request.
**Bodies are not included** — open the ones that match the work, and not the
rest.

**If the path does not exist**, the bundle is not adopted here. That is an
answer, not an error.
