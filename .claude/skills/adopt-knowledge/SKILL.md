---
name: adopt-knowledge
description: Take bundles from a catalog into a repository and make an agent aware of them. Use when setting a project up, when adding a capability, or when an agent keeps needing to be told where to look.
---

<!-- luma-foreman:generated from luma/luma-tools workflows/adopt-knowledge. Regenerate with `luma-foreman outfit`; edits are lost. -->

# Adopt knowledge into a project

**Read `.luma/bundles/luma/luma-tools/workflows/adopt-knowledge.md` and follow it.** That file is the workflow. This is the adapter that makes it reachable from here, and it deliberately carries no copy of it — the copy would drift.

Standing context this workflow assumes:

- `.luma/bundles/luma/luma-tools/policy/what-each-tool-does.md` — The tools, the one job each performs, and when to use them. Read before installing or invoking any of them.

From the `luma/luma-tools` bundle, vendored at `.luma/bundles/luma/luma-tools/`. Do not edit anything under there — an adopted bundle is a copy, and editing it is drift.
