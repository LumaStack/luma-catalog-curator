---
name: install-the-tools
description: Get foreman onto a machine and wired into a harness. Use on a new workstation, after an upgrade, or when a permission gate is not firing.
---

<!-- luma-foreman:generated from luma/luma-tools workflows/install-the-tools. Regenerate with `luma-foreman outfit`; edits are lost. -->

# Install the luma tools

**Read `.luma/bundles/luma/luma-tools/workflows/install-the-tools.md` and follow it.** That file is the workflow. This is the adapter that makes it reachable from here, and it deliberately carries no copy of it — the copy would drift.

Standing context this workflow assumes:

- `.luma/bundles/luma/luma-tools/policy/what-each-tool-does.md` — The tools, the one job each performs, and when to use them. Read before installing or invoking any of them.
- `.luma/bundles/luma/luma-tools/workflows/adopt-knowledge.md` — Take bundles from a catalog into a repository and make an agent aware of them. Use when setting a project up, when adding a capability, or when an agent keeps needing to be told where to look.

From the `luma/luma-tools` bundle, vendored at `.luma/bundles/luma/luma-tools/`. Do not edit anything under there — an adopted bundle is a copy, and editing it is drift.
