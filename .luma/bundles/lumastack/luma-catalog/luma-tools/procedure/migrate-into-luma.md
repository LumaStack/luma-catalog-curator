---
type: procedure
type_version: "0.0.1"
title: Migrate into luma
description: Move an existing project's scattered conventions, decisions and notes into .luma/. Use on a project that already has this material somewhere else.
---

# Migrate into luma

Most projects already hold this material — in a `docs/` folder, a wiki, a long
`CONTRIBUTING.md`, or somebody's head. Migration is mostly sorting, and the
sorting rule is lifecycle.

## 1. Sort by lifecycle, not by topic

For each thing you find, ask **which of these it is** — not what it is about:

| if it | it goes in |
| --- | --- |
| states an intention nobody has acted on | `backlog/` |
| is currently in force | `bundles/` |
| happened, and is dated | `records/` |
| configures a tool | `config/` |

A glossary and a guardrail both go in the same place. They are not similar; they
have the same lifecycle, which is the only axis that decides location.

## 2. Do not move what you have not read

A migration is the moment somebody finally reads the four-year-old convention
document. **Half of it will be wrong**, and moving it unchanged launders stale
advice into the one place agents are told to trust.

Read each thing. Move it, fix it, or drop it — and record dropping it, because
*we deliberately stopped doing this* is more useful than silence.

## 3. What is in force becomes a bundle

Anything that survives step 2 and is currently in force goes into a bundle in
your own namespace:

```
.luma/bundles/<your-org>/<name>/
  BUNDLE.md
  policy/
  procedure/
```

That is four extra lines of manifest, and it makes promotion a directory copy if
another project ever wants the same thing.

## 4. Leave a pointer where the material was

Delete the old file, but not silently. A one-line pointer in its place —
*moved to `.luma/bundles/…`* — costs nothing and stops the next person
recreating it from memory.

**Do not leave the content in both places.** Two copies of a rule drift, and
nobody can tell which is current.

## 5. Do not migrate history

Old decisions and old incidents are records, and records are dated and
append-only. **Backfilling them with today's date is a lie about when you knew
something** — which is the one thing records exist to get right.

Either move them with their original dates intact, or leave them where they are
and point at them. A record whose date you invented is worse than one you did
not move.

## 6. Verify

```sh
luma-foreman inspect
```

Then commit the whole thing at once, so the move is one reviewable change rather
than a fortnight of files quietly relocating.
