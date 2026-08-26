"""Rendering findings, and the doctor.

**Two outputs with opposite contracts, which is why they are two commands.**
`check` can fail — its exit code is what makes it a gate when something wires it
into CI. `report` never fails: individual entries are defensible and the
aggregate is what nobody sees, so refusing on it would be refusing a catalog for
being large.
"""

from __future__ import annotations

import json
import sys

from .catalog import Catalog
from .finding import Result

WIDTH = 78


def render(result: Result, as_json: bool) -> int:
    if as_json:
        print(
            json.dumps(
                {
                    "findings": [f.as_dict() for f in result.sorted_findings()],
                    "notices": [n.as_dict() for n in result.notices],
                    "skipped": [s.as_dict() for s in result.skipped],
                    "ran": result.ran,
                },
                indent=2,
            )
        )
        return 1 if result.findings else 0

    for finding in result.sorted_findings():
        print(f"{finding.severity.upper():<8}{finding.summary}")
        print(f"{'':10}check={finding.check}")
        for line in finding.evidence:
            print(f"{'':12}{line}")
        if finding.remedy:
            print(f"{'':10}{finding.remedy}")
        print()

    for notice in result.notices:
        print(f"{'NOTICE':<8}{notice.summary}")
        print(f"{'':10}check={notice.check}")
        for line in notice.evidence:
            print(f"{'':12}{line}")
        if notice.remedy:
            print(f"{'':10}{notice.remedy}")
        print()

    for skip in result.skipped:
        print(f"SKIPPED   {skip.check}: {skip.reason}")
        if skip.remedy:
            print(f"{'':10}{skip.remedy}")
        print()

    print(
        f"{len(result.findings)} finding(s) and {len(result.notices)} notice(s) "
        f"from {len(result.ran)} check(s) that ran; {len(result.skipped)} "
        f"check(s) could not run."
    )
    if result.notices:
        print("A notice is for a second reader, and never fails a run.")
    if result.skipped:
        print("A skipped check is not a pass.")
    return 1 if result.findings else 0


def doctor(cat: Catalog, as_json: bool) -> int:
    """What the catalog is becoming. A report, never a gate."""
    if cat.error:
        print(f"luma-catalog-curator: {cat.error}", file=sys.stderr)
        return 2

    rows = []
    for bundle in sorted(cat.bundles, key=lambda b: b.name):
        if bundle.error:
            continue
        rows.append(
            {
                "bundle": bundle.name,
                "version": bundle.version,
                "documents": len(bundle.docs),
                "always_on": len(bundle.always_on()),
                "always_words": bundle.always_words(),
                "legacy_field": len(bundle.legacy_docs()),
                "words": sum(d.words for d in bundle.docs),
            }
        )

    total_always = sum(r["always_words"] for r in rows)
    total_legacy = sum(r["legacy_field"] for r in rows)
    summary = {
        "catalog": str(cat.root),
        "namespace": cat.namespace or None,
        "bundles": len(rows),
        "documents": sum(r["documents"] for r in rows),
        "always_words_if_all_adopted": total_always,
        "documents_still_using_applies_to": total_legacy,
        "entries": rows,
    }

    if as_json:
        print(json.dumps(summary, indent=2))
        return 0

    name = cat.namespace or "(no namespace declared)"
    print(f"{name} — {len(rows)} bundle(s), {summary['documents']} document(s)")
    print()
    print(f"{'bundle':<26}{'version':>9}{'docs':>6}{'always':>8}{'words':>8}")
    print("-" * 57)
    for row in rows:
        print(
            f"{row['bundle']:<26}{row['version']:>9}{row['documents']:>6}"
            f"{row['always_on']:>8}{row['always_words']:>8}"
        )
    print("-" * 57)
    print(f"{'every bundle adopted':<26}{'':>9}{'':>6}{'':>8}{total_always:>8}")
    print()
    print(
        "The last column is what a bundle costs an adopter in **every session**,\n"
        "unconditionally — the sum of its `matches: always` documents. It is a\n"
        "context tax the catalog can compute and the adopter cannot see before\n"
        "adopting."
    )
    print(
        "\nZero is the expected reading. A Document that says nothing about what\n"
        "surfaces it is available on request, so this counts only what asked for\n"
        "a permanent seat."
    )

    heavy = [r for r in rows if r["always_words"] > 1200]
    if heavy:
        print()
        print("Heaviest, and worth a second look:")
        for row in sorted(heavy, key=lambda r: -r["always_words"]):
            print(f"  {row['bundle']} — {row['always_words']} words always loaded")
        print(
            "\n  A large unconditional footprint is a defect that is visible as a\n"
            "  number. Consider whether every always-on document earns it."
        )

    if total_legacy:
        print()
        print(f"{total_legacy} document(s) still say `applies_to` rather than `matches`:")
        for row in sorted((r for r in rows if r["legacy_field"]), key=lambda r: r["bundle"]):
            print(f"  {row['bundle']} — {row['legacy_field']}")
        print(
            "\n  The old name is read where the new one is absent, so nothing is\n"
            "  broken and nothing is finished. This count is the migration's\n"
            "  ledger — it goes quiet when the work is done."
        )
    return 0
