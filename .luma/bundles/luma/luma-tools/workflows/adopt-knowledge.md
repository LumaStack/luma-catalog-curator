---
type: workflow
title: Adopt knowledge into a project
description: Take bundles from a catalog into a repository and make an agent aware of them. Use when setting a project up, when adding a capability, or when an agent keeps needing to be told where to look.
compliance: optional
---

# Adopt knowledge into a project

**The whole loop is three commands**, and the third is the one people forget.

```bash
luma-foreman adopt --list --from https://github.com/LumaStack/luma-catalog
luma-foreman adopt luma/decision-records --from https://github.com/LumaStack/luma-catalog
luma-foreman outfit
```

## 1. See what is on offer

`adopt --list` prints every bundle a catalog publishes with its version and
description. **The description is what you decide on** — it is written to be
read by somebody choosing.

Set the catalog once so you stop passing `--from`:

```toml
# .luma/config/foreman.toml
[catalog]
source = "https://github.com/LumaStack/luma-catalog"
```

## 2. Adopt what the work actually needs

**Adopt few things.** Every bundle is content an agent may load, and the cost of
a bundle nobody needed is paid in every session that loads its standing rules.

A bundle lands in `.luma/bundles/<org>/<name>/` with a record in
`adopted.toml` — version, source, catalog commit, and a checksum of exactly what
arrived.

**Commit the copy.** That is what makes a fresh clone reproduce the project with
no network, and it is the difference between this and a package cache.

## 3. Project it, or nothing changes

```bash
luma-foreman outfit
```

**Adoption puts knowledge in the repository; nothing yet puts it in front of an
agent.** `outfit` writes a skill per workflow and an index of everything adopted
into `CLAUDE.md`.

**A bundle adopted and never projected is the failure that reads green from
every angle** — the directory is there, the checksum matches, the report is
clean, and no agent has ever seen it. `inspect` reports it; running `outfit`
prevents it.

Everything it writes is generated. Commit it or ignore it, but regenerate rather
than editing. Only the region between `luma:begin` and `luma:end` in `CLAUDE.md`
is touched, so a hand-written file keeps the rest.

## 4. Keep it honest

```bash
luma-foreman inspect --rule adoption
```

Three ways a copy stops being what you adopted: **edited** in place, **missing**
from disk, and **adopted but reaching no agent**.

**It cannot tell you whether a newer version exists.** That needs the catalog,
and inspection runs offline by design. Re-run `adopt` to find out.

## When a bundle is nearly right

**Do not edit it.** The next adoption discards the change and upstream never
learns anybody wanted it — `adopt` refuses rather than overwriting, which is how
you find out.

Two honest options. **Send it upstream**, to the catalog it came from, so every
adopter gets it. Or **fork it into your own namespace** —
`.luma/bundles/<yours>/<name>/` — which makes it your content, yours to change,
and yours to maintain.

## Upgrading

Re-run `adopt`. A newer version is an upgrade and is reported as one; the same
version is a no-op. **Read what changed before committing** — for prose, a
two-character diff can reverse a rule, so the version tier is a signal rather
than a guarantee.
