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
        mandatory = [d for d in bundle.docs if d.preload == "mandatory"]
        rows.append(
            {
                "bundle": bundle.name,
                "version": bundle.version,
                "documents": len(bundle.docs),
                "preload_mandatory": len(mandatory),
                "preload_words": bundle.preload_words(),
                "words": sum(d.words for d in bundle.docs),
            }
        )

    total_preload = sum(r["preload_words"] for r in rows)
    summary = {
        "catalog": str(cat.root),
        "namespace": cat.namespace or None,
        "bundles": len(rows),
        "documents": sum(r["documents"] for r in rows),
        "preload_words_if_all_adopted": total_preload,
        "entries": rows,
    }

    if as_json:
        print(json.dumps(summary, indent=2))
        return 0

    name = cat.namespace or "(no namespace declared)"
    print(f"{name} — {len(rows)} bundle(s), {summary['documents']} document(s)")
    print()
    print(f"{'bundle':<26}{'version':>9}{'docs':>6}{'preload':>9}{'words':>8}")
    print("-" * 58)
    for row in rows:
        print(
            f"{row['bundle']:<26}{row['version']:>9}{row['documents']:>6}"
            f"{row['preload_mandatory']:>9}{row['preload_words']:>8}"
        )
    print("-" * 58)
    print(f"{'every bundle adopted':<26}{'':>9}{'':>6}{'':>9}{total_preload:>8}")
    print()
    print(
        "The last column is what a bundle costs an adopter in **every session**,\n"
        "unconditionally — the sum of its `preload: mandatory` documents. It is a\n"
        "context tax the catalog can compute and the adopter cannot see before\n"
        "adopting."
    )

    heavy = [r for r in rows if r["preload_words"] > 1200]
    if heavy:
        print()
        print("Heaviest, and worth a second look:")
        for row in sorted(heavy, key=lambda r: -r["preload_words"]):
            print(f"  {row['bundle']} — {row['preload_words']} words always loaded")
        print(
            "\n  A large unconditional footprint is a defect that is visible as a\n"
            "  number. Consider whether every mandatory document earns it."
        )
    return 0
