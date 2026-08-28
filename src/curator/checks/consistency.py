"""Contradictions only the catalog can see.

**This is the whole reason the curator exists rather than being a foreman rule.**
Every check here is *meaningless about one bundle*: it asks whether a set of
declarations can all be true at once, which needs the set.

`DECISIONS.md` calls these **the one error class the catalog can commit that no
individual project could ever detect** — and the reason to catch them at
publication is that publication is where the only person who can fix them is
standing. Letting one through means it surfaces in front of an adopter who owns
neither bundle and whose only recourse is forking.
"""

from __future__ import annotations

from ..catalog import Catalog
from ..finding import Finding, Result, Skipped

CHECK = "consistency"

OBLIGATIONS = ("mandatory", "recommended", "optional", "deprecated")


def run(cat: Catalog) -> Result:
    if cat.error:
        # Reported once by `manifest`; repeating it here would teach people to
        # skim findings.
        return Result(skipped=[Skipped(CHECK, cat.error, "See the manifest check.")])

    result = Result(ran=[CHECK])

    def bad(sev: str, summary: str, evidence: list[str], remedy: str) -> None:
        result.findings.append(
            Finding(CHECK, sev, summary, tuple(sorted(evidence)[:10]), remedy)
        )

    # --- a bundle both mandated and deprecated -----------------------------
    #
    # Not a precedence puzzle. `deprecated` states something about the bundle's
    # future rather than its strength, so it is not on the most-restrictive-wins
    # ladder at all — a catalog saying both is simply broken.
    strength: dict[str, set[str]] = {}
    unknown: list[str] = []
    for entry in cat.requires:
        bundle = str(entry.get("bundle", "")).strip()
        obligation = str(entry.get("obligation", "")).strip()
        if not bundle:
            continue
        if obligation and obligation not in OBLIGATIONS:
            unknown.append(f"{bundle}: {obligation}")
        strength.setdefault(bundle, set()).add(obligation)

    contradictory = [
        b for b, o in strength.items() if "deprecated" in o and "mandatory" in o
    ]
    if contradictory:
        bad(
            "high",
            f"{len(contradictory)} bundle(s) both mandated and deprecated",
            contradictory,
            "deprecated says something about a bundle's future and mandatory "
            "about its strength, so they are not two points on one ladder. "
            "Decide which is true and remove the other entry.",
        )

    if unknown:
        bad(
            "medium",
            f"{len(unknown)} requirement(s) use an unknown obligation",
            unknown,
            f"Obligations are {', '.join(OBLIGATIONS)}. A value outside the "
            "ladder resolves against nothing, so the requirement silently does "
            "not apply.",
        )

    # --- requirements naming bundles nobody publishes ----------------------
    #
    # A requirement that names nothing cannot be satisfied and cannot be
    # reported as unmet in any useful way. A namespaced foreign bundle is
    # legitimate — an upstream chain is real — so only unqualified names and
    # this catalog's own namespace are checked.
    dangling = [
        b
        for b in strength
        if (("/" not in b) or (cat.namespace and b.startswith(f"{cat.namespace}/")))
        and not cat.publishes(b)
    ]
    if dangling:
        bad(
            "high",
            f"{len(dangling)} requirement(s) name a bundle this catalog does not publish",
            dangling,
            "An obligation on a bundle nobody can adopt fails every consumer "
            "and can never be satisfied. Publish it, or drop the requirement.",
        )

    # --- tags outside the published vocabulary -----------------------------
    #
    # The vocabulary is published rather than free-form precisely so this can be
    # an error. A requirement tagged with a word no consumer can declare never
    # fires, and everything still reports green — which the type calls the worst
    # failure available here.
    if cat.tags:
        vocabulary = set(cat.tags)
        stray: list[str] = []
        for entry in cat.requires:
            tags = entry.get("tags", [])
            if not isinstance(tags, list):
                continue
            for tag in tags:
                if str(tag) not in vocabulary:
                    stray.append(f"{entry.get('bundle', '?')}: {tag}")
        if stray:
            bad(
                "high",
                f"{len(stray)} requirement tag(s) are outside the published vocabulary",
                stray,
                "A consumer can only declare a tag this catalog publishes, so a "
                "requirement keyed on anything else never fires — and nothing "
                "reports that it did not.",
            )


    return result


# **Nothing calls these two, and that is a decision somebody has to make.** They
# compared a starter's pin against this catalog's own mandate, and starters are
# withdrawn. Deleting them is defensible — uncalled code is the same defect the
# withdrawal was about — and so is keeping them, because `requires` entries
# still carry `version:` constraints and **nothing anywhere verifies that an
# adopted bundle satisfies one.** This is the only built piece of that check.
#
# Left in place rather than deleted quietly, so the choice is made deliberately
# instead of by whoever notices first.
def _satisfies(version: str, constraint: str) -> bool:
    """Whether an exact *version* satisfies a simple *constraint*.

    **Deliberately narrow, and it reports only what it is sure of.** Comparison
    handles `>=`, `>`, `<=`, `<`, `==` and a bare exact version against
    dot-separated numeric parts. Anything else — a range, a caret, a wildcard —
    returns True, because a checker that guessed at an expression it does not
    implement would refuse a catalog for a constraint that is actually fine.

    A false negative here is somebody's publication blocked by a bug. A false
    positive is a conflict caught later by the same rule, once the expression
    grammar is settled. Those costs are not symmetric.
    """
    constraint = constraint.strip()
    for op in (">=", "<=", "==", ">", "<"):
        if constraint.startswith(op):
            wanted = constraint[len(op) :].strip()
            got, exp = _parts(version), _parts(wanted)
            if got is None or exp is None:
                return True
            return {
                ">=": got >= exp,
                "<=": got <= exp,
                "==": got == exp,
                ">": got > exp,
                "<": got < exp,
            }[op]
    if all(c.isdigit() or c == "." for c in constraint):
        return version.strip() == constraint
    return True


def _parts(version: str) -> tuple[int, ...] | None:
    try:
        return tuple(int(p) for p in version.strip().split("."))
    except ValueError:
        return None
