"""The checks the curator knows about.

A dict, not a configuration format. Nothing yet wants configuring: every check
is shape-based, every one runs on any catalog, and none has a knob worth
exposing. The moment one needs per-catalog tuning is the moment to design a
schema — and not before, because a schema drawn around today's checks would be
wrong in ways nobody can see yet.

**`manifest` runs first deliberately.** If the catalog does not parse, it says
so once and everything after it skips, rather than each check reporting its own
version of the same failure.

**`REF_CHECKS` is a second group because those checks need a second tree.**
Everything in `CHECKS` is answerable from the catalog on disk. A check about
what *changed* is only answerable against something to compare with, so it runs
when the caller names one and is otherwise absent — absent rather than skipped,
because a skipped check prints a warning and there is nothing to warn about
when nobody asked for a comparison.
"""

from __future__ import annotations

from ..catalog import Catalog
from ..finding import Result
from . import consistency, manifest, routing, versioning

CHECKS = {
    manifest.CHECK: manifest.run,
    consistency.CHECK: consistency.run,
    routing.CHECK: routing.run,
}

# Checks that compare the catalog against a git ref. Only run with `--against`.
REF_CHECKS = {
    versioning.CHECK: versioning.run,
}

ALL = {**CHECKS, **REF_CHECKS}


def run(cat: Catalog, only: str | None = None, against: str | None = None) -> Result:
    result = Result()
    for name, check in CHECKS.items():
        if only and name != only:
            continue
        result.extend(check(cat))
    if against is not None:
        for name, check in REF_CHECKS.items():
            if only and name != only:
                continue
            result.extend(check(cat, against))
    return result
