---
type: procedure
type_version: "0.0.1"
title: Initialize luma
description: Stand up .luma/ in a repository that does not have one. Install foreman if it is missing, then run init. Use when setting up luma in a project for the first time.
---

# Initialize luma

**`luma-foreman init` does this.** The procedure exists to get you to that
command, not to reproduce it — what the directory *holds* is the
`luma-directory-layout` policy in the `luma-layout` bundle; what makes it is the
tool's business.

## 1. Stop if there is one already

```bash
ls -d .luma 2>/dev/null
```

`init` refuses a repository that has one. To move an existing structure in, use
[[migrate-into-luma]].

## 2. Get foreman if it is missing

```bash
luma-foreman --help || {
  git clone https://github.com/LumaStack/luma-foreman.git
  ln -s "$PWD/luma-foreman/bin/luma-foreman" ~/.local/bin/luma-foreman
}
```

*Repeated rather than referenced so this runs without another bundle adopted.
`install-the-tools` in `luma-tools` is the depth — upgrades, harness wiring, the
other tools — and is not required here.*

## 3. Initialize

```bash
luma-foreman init --catalog https://github.com/LumaStack/luma-catalog
```

Writes `.luma/PROJECT.md` and `.luma/config/luma-foreman.toml`, and nothing
else. `bundles/` arrives on the first `get`, `records/` on the first record.

## 4. Fill in `PROJECT.md`, then commit

**Only you can write it** — what this repository is, for something outside it. A
skeleton nobody completed reads as an answer, which is worse than none.

Commit `.luma/` in full; it is never ignored.

## 5. Adopt

```bash
luma-foreman get lumastack/luma-catalog/<bundle>
luma-foreman apply
```

Never hand-write `adopted.toml` — it is tool-written, and a hand-made one
disagrees with reality the moment anything is adopted.
