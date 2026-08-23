"""The little bit of git the curator needs, and nothing more.

**Reading a catalog from disk is not enough to answer "what changed".** A
version is only honest relative to something — the same files at some earlier
point — so a check about versions needs a second copy of the catalog to compare
against, and git already has every one of them.

**This shells out rather than reading `.git/` directly.** Parsing object
storage to save one process would be reimplementing git badly in a tool whose
whole premise is that it carries no dependencies. `git` is present wherever a
catalog is.

**Every failure here raises rather than returning a value.** A comparison that
could not be made must never be reported as a comparison that found nothing,
which is the same reason `Skipped` exists — except that a caller who asked for
`--against` explicitly asked for this, so it is a usage error rather than a
skip.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


class GitError(Exception):
    """git could not answer, and the caller must not pretend otherwise."""


def _run(root: Path, *args: str) -> str:
    try:
        done = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:  # git is not installed
        raise GitError(f"could not run git: {exc}") from exc
    if done.returncode != 0:
        detail = (done.stderr or done.stdout).strip().splitlines()
        raise GitError(detail[0] if detail else f"git {args[0]} failed")
    return done.stdout


def repo_root(start: Path) -> Path:
    """The working tree *start* is inside."""
    out = _run(start, "rev-parse", "--show-toplevel").strip()
    if not out:
        raise GitError(f"not inside a git working tree: {start}")
    return Path(out)


def resolve(root: Path, ref: str) -> str:
    """*ref* as a commit SHA, or raise saying it is not a commit here."""
    try:
        return _run(root, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}").strip()
    except GitError:
        raise GitError(
            f"no such commit: {ref} — nothing to compare against. "
            "In a pre-merge job, fetch the base branch first."
        ) from None


def changed(root: Path, ref: str, within: Path) -> set[str]:
    """Repository-relative paths under *within* that differ from *ref*.

    **Untracked files count.** Adding a document to a bundle and forgetting to
    `git add` it is still a change to that bundle, and a check that only looked
    at tracked content would report clean on the exact working tree the author
    is looking at. A pre-merge job sees no untracked files, so this costs
    nothing there and saves the local run from lying.
    """
    relative = within.relative_to(root).as_posix()
    scope = ["--", relative] if relative not in ("", ".") else []
    out = set(_run(root, "diff", "--name-only", ref, *scope).split("\n"))
    out |= set(
        _run(root, "ls-files", "--others", "--exclude-standard", *scope).split("\n")
    )
    return {line for line in out if line}


def file_at(root: Path, ref: str, path: Path) -> str | None:
    """A file's contents at *ref*, or None if it did not exist there."""
    relative = path.relative_to(root).as_posix()
    try:
        return _run(root, "show", f"{ref}:{relative}")
    except GitError:
        return None
