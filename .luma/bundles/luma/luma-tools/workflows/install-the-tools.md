---
type: workflow
title: Install the luma tools
description: Get foreman onto a machine and wired into a harness. Use on a new workstation, after an upgrade, or when a permission gate is not firing.
---

# Install the luma tools

**Only install what you will use.** `foreman` is the one nearly everybody
needs; the rest are independent and none of them depend on each other.

## 1. Check what you already have

```bash
luma-foreman help
```

If that works, skip to step 3 — you are upgrading rather than installing.

## 2. Clone and link

Each tool runs straight from a checkout. No build step and no dependencies to
install; `foreman` needs Python 3.11+ and git.

```bash
git clone https://github.com/LumaStack/luma-foreman.git
ln -s "$PWD/luma-foreman/bin/luma-foreman" ~/.local/bin/luma-foreman
```

**There are no releases and no tags yet**, so a clone tracks `main`. That is a
real limitation rather than a preference: you cannot pin a tool version, and
upgrading means pulling.

## 3. Wire the permission gate, if you want it

```bash
luma-foreman agent-permissions install
```

**It installs the gate and then prints what to change in
`~/.claude/settings.json` rather than editing that file.** A tool writes freely
into a directory it owns and never silently edits configuration you own — so
this step is deliberately not automatic, and the output is the instruction.

Hook wiring needs a harness restart. Permission changes after that are live,
because the gate re-reads its files on every call.

```bash
luma-foreman agent-permissions doctor
```

**Run this rather than assuming.** A permission gate that is installed but not
wired fails **open** — it permits everything and reports nothing, which looks
identical to working.

## 4. Confirm, in a real repository

```bash
cd <a repository you care about>
luma-foreman inspect
```

Exit `0` is nothing found, `1` is findings, `2` is could not run. **A check that
could not run is reported as skipped and never as a pass**, so read the skips.

## Upgrading

`git pull` in the checkout, then re-run `agent-permissions install` — it is
idempotent and says when there is nothing to do. **Re-run it after every
upgrade**, because a gate left on disk from a previous version is an older set
of rules that is still present and still runnable.
