---
name: prune-archived-decisions
description: Permanently remove decision records that have been archived longer than the retention period. Only reaches `archived/`, never a live decision. Rarely the right call.
---

<!-- luma-foreman:generated from luma/decision-records workflows/prune-archived-decisions. Regenerate with `luma-foreman outfit`; edits are lost. -->

# Prune archived decisions

**Read `.luma/bundles/luma/decision-records/workflows/prune-archived-decisions.md` and follow it.** That file is the workflow. This is the adapter that makes it reachable from here, and it deliberately carries no copy of it — the copy would drift.

Standing context this workflow assumes:

- `.luma/bundles/luma/decision-records/policy/decision-guidelines.md` — When to record a decision, what makes one worth reading years later, and what you may edit once it is settled.
- `.luma/bundles/luma/decision-records/workflows/record-decision.md` — Find or establish where this project keeps decisions, then write one. Use when a position is settled, when an irreversible change is proposed, or when asked where decisions live.

From the `luma/decision-records` bundle, vendored at `.luma/bundles/luma/decision-records/`. Do not edit anything under there — an adopted bundle is a copy, and editing it is drift.
