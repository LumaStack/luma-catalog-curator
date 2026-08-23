---
type: workflow
title: Change a type more than one tool depends on
description: Alter a shared type without making every tool upgrade at once. Use before touching anything in luma/luma-types, or any type a second consumer already reads.
---

# Change a type more than one tool depends on

**A breaking change is never one release. It is three**, and getting that
backwards is the mistake this workflow exists to prevent.

## 1. Is it actually breaking?

**Adding a field is not.** Consumers must not reject a document for keys they do
not understand, so a new field is invisible to everything that has not learned
it. Ship it, bump the type's minor, done.

**Removing a field, renaming one, or changing what one means is breaking.** So
is changing `field_type` or the permitted `values`.

**And raising an obligation is breaking while looking additive.** Strengthening
`optional` to `mandatory` makes every existing document lacking the field
non-compliant the moment it ships. That is a contract step wearing an expand
step's clothes, and it is the one people get wrong.

## 2. Expand

**Add the new form; keep the old one. Both valid.**

Nobody has to upgrade. A tool that has never heard of the new field reads the
old one and is correct. A tool that knows both prefers the new and falls back.

**Tools are field-tolerant rather than version-aware, and have no choice** — a
document never records which type version it was written against, so version
dispatch is impossible. *Read the new field, or if absent the old one* is the
entire technique.

## 3. Migrate

**Move the documents.** This is the work, and it happens in two places that cost
very differently.

**Updating a vendored copy of the type is mechanical**, and happens once per
bundle that carries it. Record what you took in `vendored_from`.

**Migrating records already written happens once per project**, because the
records belong to the project however many bundles vendored the type. This is
the expensive hop and the one to plan around.

## 4. Contract

**Remove the old form.** This is the breaking release, and by now everyone has
already moved — which is the whole point of the previous two steps.

Bump the type's major. Bump the bundle carrying it.

## 5. Say what happened, where somebody will meet it

The bundle's `## Version` section carries the reasoning. **State what an adopter
has to do**, not only what changed.

## The one that bites

**Aggregation across projects is where a half-finished migration hurts.**
Documents inside bundles are safe by construction, because each bundle's
documents are checked against the copy that travelled with them.

**Out-of-bundle documents have no such scope.** Something reading every
project's `.luma/project.md` while half declare the old field and half the new
gets a result where every file parses, nothing errors, and **the aggregate is
silently incomplete.**

A collector should read the version each project declares and say so, rather
than presenting a mixed set as though it were uniform.

## Checking your own work

**Did you skip *expand*?** If any moment in the sequence required two tools to
ship together, you did. Go back — that is the failure the three steps exist to
remove, and it does not announce itself until somebody upgrades one thing.
