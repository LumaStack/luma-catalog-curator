---
name: change-a-shared-type
description: Alter a shared type without making every tool upgrade at once. Use before touching anything in luma/luma-types, or any type a second consumer already reads.
---

<!-- luma-foreman:generated from luma/luma-maintainers workflows/change-a-shared-type. Regenerate with `luma-foreman outfit`; edits are lost. -->

# Change a type more than one tool depends on

**Read `.luma/bundles/luma/luma-maintainers/workflows/change-a-shared-type.md` and follow it.** That file is the workflow. This is the adapter that makes it reachable from here, and it deliberately carries no copy of it — the copy would drift.

Standing context this workflow assumes:

- `.luma/bundles/luma/luma-maintainers/policy/the-estate.md` — The six repositories, the boundary each one defends, and the rule that decides where a new thing goes. Read before adding anything to any of them.

From the `luma/luma-maintainers` bundle, vendored at `.luma/bundles/luma/luma-maintainers/`. Do not edit anything under there — an adopted bundle is a copy, and editing it is drift.
