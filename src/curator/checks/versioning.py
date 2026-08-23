"""Whether what changed said so in its version.

**A version is the only promise a bundle makes, and it is made by hand.** An
adopter pins one, compares one, and decides from one whether to take a change.
A bundle whose files moved while its version stood still tells every adopter
that nothing happened — and the adopter has no way to find out otherwise short
of diffing a directory they did not write.

**This is the one check here that needs a second copy of the catalog**, which
is why it runs only when the caller supplies `--against <ref>`. Everything else
the curator does is answerable from one tree.

**It refuses to judge the tier.** Whether a change was major, minor or patch is
the author's call and stays that way — this asks only whether the number moved
at all, which is mechanical, and leaves the judgement to the person who made
the change. A tool that guessed the tier would be wrong in exactly the cases
that matter.

**A bundle that did not exist at the ref is new**, and a new bundle owes no
bump. Its first version is whatever its author wrote.
"""

from __future__ import annotations

from pathlib import Path

from .. import git, yamlish
from ..catalog import Catalog
from ..finding import Finding, Result, Skipped

CHECK = "versioning"


def _version_at(root: Path, ref: str, manifest: Path) -> tuple[str | None, str | None]:
    """The `version` a bundle declared at *ref*, and why it could not be read.

    Returns `(None, None)` when the bundle did not exist there at all, which is
    a new bundle rather than a problem.
    """
    text = git.file_at(root, ref, manifest)
    if text is None:
        return None, None
    try:
        front = yamlish.frontmatter(text)
    except yamlish.YamlishError as exc:
        return None, str(exc)
    if front is None:
        return "", None
    return str(front.get("version", "")), None


def run(cat: Catalog, against: str) -> Result:
    if cat.error:
        return Result(skipped=[Skipped(CHECK, cat.error, "See the manifest check.")])

    # Resolved throughout, because git answers in real absolute paths and a
    # relative or symlinked catalog path would not line up with them.
    here = cat.root.resolve()
    try:
        root = git.repo_root(here)
        ref = git.resolve(root, against)
        touched = git.changed(root, ref, here)
    except git.GitError as exc:
        # Loud, and not a pass. The caller asked for a comparison by name; the
        # honest answer to "I could not make it" is a finding, because the exit
        # code is the whole point of asking.
        return Result(
            ran=[CHECK],
            findings=[
                Finding(
                    CHECK,
                    "high",
                    f"could not compare against {against}",
                    (str(exc),),
                    "Nothing was compared, so no version was checked. A "
                    "pre-merge job needs the base branch fetched before this "
                    "can mean anything.",
                )
            ],
        )

    result = Result(ran=[CHECK])
    stale: list[str] = []
    unreadable: list[str] = []

    for bundle in sorted(cat.bundles, key=lambda b: b.name):
        home = bundle.root.resolve()
        prefix = f"{home.relative_to(root).as_posix()}/"
        files = sorted(p for p in touched if p.startswith(prefix))
        if not files:
            continue

        was, why = _version_at(root, ref, home / "bundle.md")
        if why:
            unreadable.append(f"{bundle.name}: bundle.md at {against}: {why}")
            continue
        if was is None:
            continue  # new bundle — its first version is whatever it says
        if was != bundle.version:
            continue

        shown = ", ".join(f[len(prefix) :] for f in files[:3])
        if len(files) > 3:
            shown += f", and {len(files) - 3} more"
        stale.append(f"{bundle.name}: still {bundle.version or '(none)'} — {shown}")

    if stale:
        result.findings.append(
            Finding(
                CHECK,
                "high",
                f"{len(stale)} bundle(s) changed without a version change",
                tuple(stale[:10]),
                "Every adopter decides whether to take a change by comparing "
                "versions, so a change that does not move the number is a "
                "change nobody can see. Bump it and say why in the bundle's "
                "`## Version` section — the tier is yours to judge, but the "
                "number has to move.",
            )
        )

    if unreadable:
        result.findings.append(
            Finding(
                CHECK,
                "medium",
                f"{len(unreadable)} bundle(s) could not be compared against {against}",
                tuple(unreadable[:10]),
                "The old manifest does not parse, so whether the version moved "
                "is unknown. These bundles were not checked.",
            )
        )

    return result
