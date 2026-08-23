"""The checks the curator knows about.

A dict, not a configuration format. Nothing yet wants configuring: every check
is shape-based, every one runs on any catalog, and none has a knob worth
exposing. The moment one needs per-catalog tuning is the moment to design a
schema — and not before, because a schema drawn around today's checks would be
wrong in ways nobody can see yet.

**`manifest` runs first deliberately.** If the catalog does not parse, it says
so once and everything after it skips, rather than each check reporting its own
version of the same failure.
"""

from __future__ import annotations

from ..catalog import Catalog
from ..finding import Result
from . import consistency, manifest

CHECKS = {
    manifest.CHECK: manifest.run,
    consistency.CHECK: consistency.run,
}


def run(cat: Catalog, only: str | None = None) -> Result:
    result = Result()
    for name, check in CHECKS.items():
        if only and name != only:
            continue
        result.extend(check(cat))
    return result
