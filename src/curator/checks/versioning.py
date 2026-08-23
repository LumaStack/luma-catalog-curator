"""Whether what changed said so in its version.

**A version is the only promise a bundle makes, and it is made by hand.** An
adopter pins one, compares one, and decides from one whether to take a change.
A bundle whose files moved while its version stood still tells every adopter
that nothing happened — and the adopter has no way to find out otherwise short
of diffing a directory they did not write.

**This is the one check here that needs a second copy of the catalog**, which
is why it runs only when the caller supplies `--against <ref>`. Everything else
the curator does is answerable from one tree.

**It refuses to judge the tier, and it does point at two signals.** Whether a
change was major, minor or patch is the author's call and stays that way. But
the version design names two things that are worth a second reader, and both
are mechanical to spot:

- **A patch that edits a normative sentence.** `must not` → `must` is two
  characters, the diff of a typo, and a complete reversal — and *"patch: fixed
  wording"* gets approved in seconds. The check cannot know whether the meaning
  changed; it can know the edit landed where meaning lives.
- **A non-major release that removes a document.** Subtraction is *"a useful
  signal that something is major, and it is not a rule"* — removing a
  carve-out is also how prose gets stronger.

**Both are notices rather than findings**, exactly as that design asks:
*"surface, never refuse."* A heuristic wired to a merge gate is a heuristic
that gets switched off.

**A bundle that did not exist at the ref is new**, and a new bundle owes no
bump. Its first version is whatever its author wrote.
"""

from __future__ import annotations

import re
from pathlib import Path

from .. import git, yamlish
from ..catalog import Catalog
from ..finding import Finding, Notice, Result, Skipped

# Where meaning lives in a normative sentence. Deliberately short: every word
# here changes what somebody is obliged to do, and a longer list would match
# ordinary prose and turn the notice into noise.
NORMATIVE = re.compile(
    r"\b(must|must not|never|always|shall|required|forbidden|may not|cannot)\b",
    re.I,
)

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
    normative: list[str] = []
    removed: list[str] = []

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
            tier = _tier(was, bundle.version)
            if tier == "patch":
                normative += _normative_edits(root, ref, home, prefix, files, bundle.name)
            if tier in ("patch", "minor"):
                removed += _removals(root, ref, prefix, files, bundle.name, was, bundle.version)
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

    if normative:
        result.notices.append(
            Notice(
                CHECK,
                f"{len(normative)} patch release(s) edited a normative sentence",
                tuple(normative[:10]),
                "A patch cannot change what anyone does. `must not` becoming "
                "`must` is two characters and a complete reversal, and it reads "
                "like a typo fix in review. Confirm the meaning held, or raise "
                "the tier. This does not fail the run.",
            )
        )

    if removed:
        result.notices.append(
            Notice(
                CHECK,
                f"{len(removed)} non-major release(s) removed a document",
                tuple(removed[:10]),
                "Removal is a signal rather than a verdict — dropping a "
                "carve-out is also how prose gets stronger. The test is whether "
                "an adopter has to do something to keep the result they had. "
                "This does not fail the run.",
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


def _tier(was: str, now: str) -> str:
    """Which part of the version moved: `major`, `minor`, `patch` or `unknown`.

    `unknown` for anything that is not two dot-separated numbers deep on both
    sides — a tool that guessed at an unfamiliar scheme would report against a
    convention its author never agreed to.
    """
    try:
        a = [int(p) for p in was.strip().split(".")]
        b = [int(p) for p in now.strip().split(".")]
    except ValueError:
        return "unknown"
    if len(a) < 2 or len(b) < 2:
        return "unknown"
    if a[0] != b[0]:
        return "major"
    if a[1] != b[1]:
        return "minor"
    return "patch"


def _normative_edits(root, ref, home, prefix, files, name) -> list[str]:
    """Changed lines carrying a normative word, in a patch release.

    A line-set comparison rather than a real diff: a line that is in one
    version and not the other has been added, removed or edited, and all three
    are worth the same second look. Moving a line unchanged is a false
    positive, and is rare enough to accept for the simplicity.
    """
    out: list[str] = []
    for rel in files:
        if not rel.endswith(".md"):
            continue
        path = root / rel
        old = git.file_at(root, ref, path)
        if old is None:
            continue  # a new document, not an edit
        try:
            new = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        before, after = set(old.split("\n")), set(new.split("\n"))
        for line in sorted((after - before) | (before - after)):
            text = line.strip()
            if text and NORMATIVE.search(text):
                out.append(f"{name}: {rel[len(prefix):]}: {text[:90]}")
    return out


def _removals(root, ref, prefix, files, name, was, now) -> list[str]:
    """Documents that existed at the ref and are gone, in a non-major release."""
    out: list[str] = []
    for rel in files:
        if not rel.endswith(".md") or (root / rel).exists():
            continue
        if git.file_at(root, ref, root / rel) is None:
            continue
        out.append(f"{name} {was} -> {now}: removed {rel[len(prefix):]}")
    return out
