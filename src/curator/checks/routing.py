"""What this catalog's rules do to the projects that adopt them.

**Cross-bundle only, which is what makes it curator's.** Whether one bundle's
triggers are well-formed is a question about that bundle, and `luma-foreman`
already answers it — an unknown trigger kind or a moment nothing fires is a
defect in a single Document and is caught there.

What no single bundle can see is what happens when several are adopted together,
and what a catalog is committing its adopters to by publishing at all. Both are
notices rather than findings: neither is wrong, and both are things a publisher
should know they are doing.
"""

from __future__ import annotations

from collections import defaultdict

from ..catalog import Catalog
from ..finding import Notice, Result, Skipped

CHECK = "routing"


def run(cat: Catalog) -> Result:
    if cat.missing or cat.error:
        return Result(
            skipped=[
                Skipped(CHECK, cat.error or "no catalog here", "Point at a catalog.")
            ]
        )

    result = Result(ran=[CHECK])

    # --- what this catalog will refuse on an adopter's behalf --------------------
    #
    # `on_violation: block` is the strongest claim a published bundle can make:
    # it stops somebody's command in a repository this catalog will never see.
    # Publishing that is a decision, and a catalog that makes it silently is a
    # catalog nobody audited.
    blocking = [
        f"{b.name} {d.doc_id} — {', '.join(d.applies_to) or 'no trigger'}"
        for b in cat.bundles
        for d in b.docs
        if d.on_violation == "block"
    ]
    if blocking:
        result.notices.append(
            Notice(
                CHECK,
                f"{len(blocking)} published rule(s) will refuse an adopter's commands",
                tuple(sorted(blocking)),
                "Blocking cannot be turned off by the projects that adopt it — that "
                "is the point of it, and the reason to be sure. An adopter's only "
                "way out is to stop adopting the bundle or to fork it.",
            )
        )

    # --- rules from different bundles that fire at the same moment ---------------
    #
    # Two bundles binding the same trigger is usually legitimate and occasionally
    # the smoke from a fire: a project adopting both gets two rules speaking at
    # once, and if they say opposite things nothing detects it. **No program can
    # read two paragraphs and conclude they disagree**, so this reports the
    # overlap and leaves the judgement to a person.
    #
    # It is scoped to `required`, because two suggestions colliding costs
    # nothing and two obligations colliding is the case worth looking at.
    where: dict[str, set[str]] = defaultdict(set)
    for bundle in cat.bundles:
        for doc in bundle.docs:
            if doc.compliance != "required":
                continue
            for trigger in doc.applies_to:
                where[trigger].add(f"{bundle.name} {doc.doc_id}")

    shared = {t: v for t, v in where.items() if len({s.split()[0] for s in v}) > 1}
    if shared:
        result.notices.append(
            Notice(
                CHECK,
                f"{len(shared)} trigger(s) bind binding rules in more than one bundle",
                tuple(sorted(f"{t} <- {', '.join(sorted(v))}" for t, v in shared.items())),
                "A project adopting both gets two obligations firing at once. That is "
                "usually fine and occasionally two rules that contradict each other — "
                "which nothing can detect automatically, because the disagreement is "
                "in the prose rather than in the triggers.",
            )
        )

    return result
