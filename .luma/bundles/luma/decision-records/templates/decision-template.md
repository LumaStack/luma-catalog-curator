# Decision record template

Copy the blocks below into `.luma/records/decisions/ADR-NNNN-kebab-title.md` —
next unused four-digit number. **Copy the blocks, not this file**: a template
carrying live frontmatter would be indexed and validated as a real decision.

Guidance is in `../policy/decision-guidelines.md`; the field contract is in
`../_types/decision.md`.

## Frontmatter

```yaml
---
type: decision
title: <short decision title, active voice>
decided: YYYY-MM-DD
lifecycle_status: provisional
reopen_trigger: <what would make this worth revisiting>
---
```

- **`decided`** — when the position became binding, **not** when the file was
  created. They are frequently different and only one is the fact people cite.
- **`lifecycle_status`** — `draft` while arguing, `provisional` once acting on
  it, `stable` when settled, `archived` when it is no longer the answer. It
  governs what you may edit; see the guidelines.
- **`superseded_by`** — add when archiving in favour of a replacement, and
  **quote it**: `superseded_by: "[[ADR-0014-the-replacement]]"`. Unquoted,
  `[[…]]` is YAML flow-sequence syntax and parses as a nested array, so the
  link silently never resolves.

## Body

```markdown
# ADR-NNNN: <short decision title, active voice>

## Summary

One sentence: what was decided.

## Problem

Why is anything being decided? The trigger, the forces, the constraints.

## Decision

What was decided — "We will …".

## Why

Observable reasoning, not assertion. "It replaces three agents with one and
speaks Prometheus, Loki and OTLP", never "it is obviously best".

<!-- Everything below is optional. Delete any section you have nothing real to
     put in — an empty heading is worse than no heading. -->

## Alternatives

Each option considered, with a one-line why-not.

## Tradeoffs

**Pros**
- …

**Cons**
- …

## Assumptions

What was believed true when deciding. If one proves false, that is a reason to
revisit — feed it into Revisit When.

## Revisit When

Concrete conditions that should reopen this. "Above 100 hosts", not "if things
change".

## Follow-up

Work this decision creates. Link to it; do not inline it.

## References

Supporting material, and related records — what this supersedes, amends, or
relates to.
```
