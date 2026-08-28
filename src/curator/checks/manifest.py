"""Whether the catalog and its bundles declare what they must.

**Structural only.** Which directories a bundle uses, how its workflows are
named, when it may call itself `1.0.0` — those are an organization's opinions,
they arrive by adoption, and a tool that compiled them in would be deciding
standards rather than checking them. Everything here follows from the shapes the
`luma/catalog` and `bundle` types define, so it holds for anybody's catalog.
"""

from __future__ import annotations

from ..catalog import Catalog
from .. import git
from ..finding import Finding, Result, Skipped

CHECK = "manifest"


def run(cat: Catalog) -> Result:
    if cat.missing:
        return Result(
            skipped=[
                Skipped(CHECK, cat.error or "no catalog here", "Point at a catalog.")
            ]
        )

    # A manifest that does not parse is a **defect in the catalog**, not a
    # limitation of the checker — so it is a finding and it fails. Reporting it
    # as skipped would print "a skipped check is not a pass" and then exit 0,
    # which is the shape of dishonesty this whole tool exists to prevent.
    if cat.error:
        return Result(
            ran=[CHECK],
            findings=[
                Finding(
                    CHECK,
                    "high",
                    "the catalog manifest could not be read",
                    (cat.error,),
                    "Nothing downstream of this ran, so a clean report below "
                    "means nothing was looked at rather than nothing was found.",
                )
            ],
        )

    result = Result(ran=[CHECK])

    def bad(sev: str, summary: str, evidence: list[str], remedy: str) -> None:
        result.findings.append(
            Finding(CHECK, sev, summary, tuple(sorted(evidence)[:10]), remedy)
        )

    declared = str(cat.manifest.get("type", ""))
    if declared and not declared.endswith("catalog"):
        bad(
            "medium",
            f"CATALOG.md declares type {declared}",
            [f"CATALOG.md: type: {declared}"],
            "The document at a catalog's root is the thing authoritative about "
            "starters, requires and the namespace. A different type means "
            "nothing will read it as a catalog.",
        )

    # A declared namespace is optional now: `luma-foreman` derives one from
    # where the catalog lives, which is what stops a fork inheriting somebody
    # else's name. Silence is only a defect where nothing can be derived —
    # a catalog with no remote, which no adopter can address at all.
    if not cat.namespace and not git.origin(cat.root):
        bad(
            "medium",
            "this catalog has no namespace and none can be derived",
            ["CATALOG.md"],
            "Every bundle is addressed <namespace>/<name>. A namespace derives "
            "from the catalog's remote; this one has none, so there is nothing "
            "to derive from and nothing declared. Add `namespace:` to "
            "CATALOG.md, or publish this where it has an address.",
        )

    if not cat.bundles:
        result.skipped.append(
            Skipped(
                CHECK,
                "this catalog publishes no bundles",
                "Nothing named BUNDLE.md under bundles/.",
            )
        )
        return result

    broken = [f"{b.name}: {b.error}" for b in cat.bundles if b.error]
    if broken:
        bad(
            "high",
            f"{len(broken)} bundle manifest(s) could not be read",
            broken,
            "A manifest nothing can parse cannot be pinned, compared, or "
            "reported on, and every check about this bundle silently did not run.",
        )

    unversioned = [b.name for b in cat.bundles if not b.error and not b.version]
    if unversioned:
        bad(
            "high",
            f"{len(unversioned)} bundle(s) declare no version",
            unversioned,
            "A bundle without a version cannot be pinned, compared, or reported "
            "as outdated — an adopter can say nothing honest about it, and this "
            "tool cannot either.",
        )

    undescribed = [b.name for b in cat.bundles if not b.error and not b.description]
    if undescribed:
        bad(
            "medium",
            f"{len(undescribed)} bundle(s) have no description",
            undescribed,
            "A description is what somebody reads when deciding whether to "
            "adopt, and what an index shows in place of the content. Without "
            "one the bundle is invisible to everything but a directory listing.",
        )

    # `entrypoint` carries a Document ID — the path within the bundle without
    # the suffix. One that resolves to nothing sends a reader nowhere, silently.
    dangling: list[str] = []
    for bundle in cat.bundles:
        if bundle.error or not bundle.entrypoint:
            continue
        ids = {d.doc_id for d in bundle.docs}
        if bundle.entrypoint not in ids:
            dangling.append(f"{bundle.name}: {bundle.entrypoint}")
    if dangling:
        bad(
            "high",
            f"{len(dangling)} entrypoint(s) point at nothing",
            dangling,
            "entrypoint carries a full Document ID — the path within the "
            "bundle, without the .md suffix.",
        )

    return result
