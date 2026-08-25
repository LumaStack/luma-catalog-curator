"""luma-catalog-curator — the entrypoint.

**Whether this is a gate or a report is not the tool's decision.** The design
document treats that as the first thing to settle and frames it as either/or;
the answer is that it is settled by the wiring rather than by the code. `check`
returns 0, 1 or 2, so a pre-merge job makes it a gate and a person at a terminal
makes it a report — the same shape foreman already uses, and the same reason.

What the tool *does* have to decide is that **an unenforced check is
decoration**. So `check` is built to be wired, and says so when it is not.
"""

from __future__ import annotations

import sys
from pathlib import Path

from . import catalog, report
from .checks import ALL, REF_CHECKS, run

USAGE = """usage: luma-catalog-curator <job> [args]

  check [<path>]     refuse what a catalog cannot hold consistently
                     ...and with --against <ref>, what changed without saying so
  report [<path>]    what the catalog is becoming — never fails

A catalog is found at <path>/CATALOG.md or <path>/catalog/CATALOG.md, and
defaults to the current directory.

Run `luma-catalog-curator <job> --help` for a job's own options."""

CHECK_USAGE = """Refuse what only the catalog can see.

  luma-catalog-curator check [<path>]         check a catalog (default: here)
  luma-catalog-curator check --json           machine-readable, for a pre-merge job
  luma-catalog-curator check --only <name>    run one check
  luma-catalog-curator check --against <ref>  ...and what changed since <ref>

Checks: {checks}

`--against <ref>` compares the working tree with a git ref and adds the checks
that are meaningless without one — today, that a bundle whose files moved said
so in its version. In a pre-merge job the ref is the base branch. Without it,
nothing here reads git at all.

Exit codes: 0 nothing found, 1 findings, 2 could not run.

**This does not check whether a bundle is internally sound** — a dangling link,
an unquoted frontmatter wikilink, a template carrying live frontmatter. Those
are properties of one bundle and need no catalog to find; `luma-foreman inspect`
already reports them. The curator checks a *set*."""

REPORT_USAGE = """What the catalog is becoming.

  luma-catalog-curator report [<path>]
  luma-catalog-curator report --json

A doctor, not a gate — it always exits 0 when it can run. Individual entries are
defensible and the aggregate is what nobody sees."""


def _err(message: str) -> int:
    print(f"luma-catalog-curator: {message}", file=sys.stderr)
    return 2


def _args(
    argv: list[str], usage: str, refs: bool = False
) -> tuple[Path, bool, str | None, str | None] | int:
    as_json = False
    only: str | None = None
    against: str | None = None
    target = Path.cwd()
    rest = list(argv)
    while rest:
        arg = rest.pop(0)
        if arg in ("-h", "--help"):
            print(usage)
            return 0
        if arg == "--json":
            as_json = True
        elif arg == "--only":
            if not rest:
                return _err("--only needs a check name")
            only = rest.pop(0)
        elif arg == "--against" and refs:
            if not rest:
                return _err("--against needs a git ref")
            against = rest.pop(0)
        elif arg.startswith("-"):
            return _err(f"unknown option: {arg}")
        else:
            target = Path(arg)
    if not target.is_dir():
        return _err(f"not a directory: {target}")
    return target, as_json, only, against


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    job = argv[0] if argv else "help"

    if job in ("help", "-h", "--help"):
        print(USAGE)
        return 0

    if job == "check":
        parsed = _args(argv[1:], CHECK_USAGE.format(checks=", ".join(ALL)), refs=True)
        if isinstance(parsed, int):
            return parsed
        target, as_json, only, against = parsed
        if only and only not in ALL:
            return _err(f"unknown check: {only} (known: {', '.join(ALL)})")
        # Asking for a ref check without a ref would run nothing and report a
        # clean zero, which is the one answer that must never be reachable by
        # getting the invocation wrong.
        if only in REF_CHECKS and against is None:
            return _err(f"check {only} needs --against <ref> — it compares two trees")
        cat = catalog.load(target)
        # No catalog here is a usage error rather than a clean result. Exiting 0
        # would tell a pre-merge job that a directory containing no catalog
        # passed, which is the one answer that is never true.
        if cat.missing:
            return _err(cat.error or "no catalog here")
        return report.render(run(cat, only, against), as_json)

    if job == "report":
        parsed = _args(argv[1:], REPORT_USAGE)
        if isinstance(parsed, int):
            return parsed
        target, as_json, _, _ = parsed
        return report.doctor(catalog.load(target), as_json)

    print(f"luma-catalog-curator: unknown job: {job}", file=sys.stderr)
    print(USAGE, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
