#!/bin/sh
# Tests for luma-catalog-curator.
#
#   sh tests/curator-test.sh
#
# Every case builds a throwaway catalog with known contents, so these assert
# what the checks actually detect rather than what they were meant to. Nothing
# here reads the real catalog.
#
# The load-bearing cases are the negative ones. A checker that finds problems is
# easy; one that stays quiet on a good catalog is the hard half, and a false
# positive in something wired pre-merge gets the check switched off.
set -u

ROOT=$(cd "$(dirname "$0")/.." && pwd -P)
CLI=${CURATOR_CLI:-$ROOT/bin/luma-catalog-curator}
export PYTHONDONTWRITEBYTECODE=1

T=$(mktemp -d /tmp/curator.XXXXXX) || exit 2
trap 'rm -rf "$T"' EXIT INT TERM

pass=0 fail=0
ok()  { pass=$((pass + 1)); }
bad() { fail=$((fail + 1)); printf 'FAIL  %s\n' "$1"; }

has()   { case $LAST in *"$1"*) ok ;; *) bad "expected output to contain '$1'" ;; esac; }
lacks() { case $LAST in *"$1"*) bad "expected output NOT to contain '$1'" ;; *) ok ;; esac; }

# check <label> <expect-exit> <args...>
check() {
  label=$1 want=$2; shift 2
  LAST=$("$CLI" check "$@" 2>&1); got=$?
  [ "$got" -eq "$want" ] && ok || bad "$label (exit $got, wanted $want): $LAST"
}

report() {
  label=$1 want=$2; shift 2
  LAST=$("$CLI" report "$@" 2>&1); got=$?
  [ "$got" -eq "$want" ] && ok || bad "$label (exit $got, wanted $want): $LAST"
}

# catalog <name> — a directory with one good bundle. Echoes the path.
catalog() {
  d=$T/$1
  mkdir -p "$d/bundles/widgets/workflows" "$d/bundles/widgets/policy"
  cat > "$d/catalog.md" <<'EOF'
---
type: luma/catalog
namespace: acme
description: A catalog.
tags:
  - service
  - library
---
EOF
  cat > "$d/bundles/widgets/bundle.md" <<'EOF'
---
type: bundle
version: 0.1.0
entry_point: workflows/make-a-widget
description: Widgets.
---
EOF
  cat > "$d/bundles/widgets/workflows/make-a-widget.md" <<'EOF'
---
type: workflow
title: Make a widget
description: Produce one.
---
Steps.
EOF
  cat > "$d/bundles/widgets/policy/rules.md" <<'EOF'
---
type: policy
title: Rules
description: What a widget may be.
preload: mandatory
---
Some rules here, which are several words long.
EOF
  printf '%s' "$d"
}

# front <catalog> <frontmatter> — replace catalog.md's frontmatter
front() { printf -- '---\n%s\n---\n' "$2" > "$1/catalog.md"; }

# --- a good catalog stays quiet ------------------------------------------------

good=$(catalog good)
check 'good catalog' 0 "$good"
has '0 finding(s)'
lacks 'HIGH'

# Found one level down, because a repository keeps content under catalog/.
mkdir -p "$T/repo" && cp -R "$good" "$T/repo/catalog"
check 'found under catalog/' 0 "$T/repo"

# No catalog here is could-not-run, never a pass: exiting 0 would tell a
# pre-merge job that a directory containing no catalog was fine.
check 'not a catalog' 2 "$T"
has 'no catalog here'

check 'no such directory' 2 "$T/nowhere"
has 'not a directory'

# --- the contradiction only a catalog can see ----------------------------------

d=$(catalog contradiction)
front "$d" 'type: luma/catalog
namespace: acme
requires:
  - bundle: acme/widgets
    obligation: mandatory
  - bundle: acme/widgets
    obligation: deprecated'
check 'mandated and deprecated' 1 "$d"
has 'both mandated and deprecated'

# --- requirements and starters that name nothing --------------------------------

d=$(catalog dangling)
front "$d" 'type: luma/catalog
namespace: acme
requires:
  - bundle: acme/nonexistent
    obligation: recommended'
check 'requirement names nothing' 1 "$d"
has 'does not publish'

# A foreign namespace is legitimate — an upstream chain is real.
d=$(catalog foreign)
front "$d" 'type: luma/catalog
namespace: acme
requires:
  - bundle: upstream/change-review
    obligation: recommended'
check 'foreign namespace not flagged' 0 "$d"
lacks 'does not publish'

d=$(catalog badstarter)
front "$d" 'type: luma/catalog
namespace: acme
starters:
  project:
    - acme/widgets
    - acme/missing'
check 'starter names nothing' 1 "$d"
has 'starter'

d=$(catalog goodstarter)
front "$d" 'type: luma/catalog
namespace: acme
starters:
  project:
    - acme/widgets'
check 'good starter is quiet' 0 "$d"

# --- tags outside the published vocabulary --------------------------------------

d=$(catalog tags)
front "$d" 'type: luma/catalog
namespace: acme
tags:
  - service
requires:
  - bundle: acme/widgets
    obligation: mandatory
    tags: [infrastructure]'
check 'tag outside vocabulary' 1 "$d"
has 'outside the published vocabulary'

d=$(catalog goodtags)
front "$d" 'type: luma/catalog
namespace: acme
tags:
  - service
requires:
  - bundle: acme/widgets
    obligation: mandatory
    tags: [service]'
check 'tag in vocabulary is quiet' 0 "$d"

# --- a starter pinning what the catalog itself forbids --------------------------

d=$(catalog pin)
front "$d" 'type: luma/catalog
namespace: acme
starters:
  project:
    adds:
      - bundle: acme/widgets
        version: "0.1.0"
requires:
  - bundle: acme/widgets
    obligation: mandatory
    version: ">= 2.0.0"'
check 'starter pin conflicts with mandate' 1 "$d"
has 'conflict'

# A pin that satisfies the mandate is fine.
d=$(catalog goodpin)
front "$d" 'type: luma/catalog
namespace: acme
starters:
  project:
    adds:
      - bundle: acme/widgets
        version: "2.1.0"
requires:
  - bundle: acme/widgets
    obligation: mandatory
    version: ">= 2.0.0"'
check 'satisfying pin is quiet' 0 "$d"
lacks 'conflict'

# A bare exact version is a constraint too, and the common shape for a mandate
# that must not move.
d=$(catalog exactpin)
front "$d" 'type: luma/catalog
namespace: acme
starters:
  project:
    adds:
      - bundle: acme/widgets
        version: "0.1.0"
requires:
  - bundle: acme/widgets
    obligation: mandatory
    version: "2.0.0"'
check 'exact constraint, wrong pin' 1 "$d"
has 'conflict'

d=$(catalog exactmatch)
front "$d" 'type: luma/catalog
namespace: acme
starters:
  project:
    adds:
      - bundle: acme/widgets
        version: "2.0.0"
requires:
  - bundle: acme/widgets
    obligation: mandatory
    version: "2.0.0"'
check 'exact constraint, matching pin' 0 "$d"
lacks 'conflict'

# An expression the comparator does not implement must not be refused.
d=$(catalog caret)
front "$d" 'type: luma/catalog
namespace: acme
starters:
  project:
    adds:
      - bundle: acme/widgets
        version: "0.1.0"
requires:
  - bundle: acme/widgets
    obligation: mandatory
    version: "^2 || ~3"'
check 'unimplemented constraint is not refused' 0 "$d"

# --- manifest shape -------------------------------------------------------------

d=$(catalog nonamespace)
front "$d" 'type: luma/catalog
description: No namespace here.'
check 'missing namespace' 1 "$d"
has 'no namespace'

d=$(catalog noversion)
printf -- '---\ntype: bundle\ndescription: No version.\n---\n' > "$d/bundles/widgets/bundle.md"
check 'bundle without a version' 1 "$d"
has 'declare no version'

d=$(catalog badentry)
printf -- '---\ntype: bundle\nversion: 0.1.0\nentry_point: workflows/nope\ndescription: x\n---\n' \
  > "$d/bundles/widgets/bundle.md"
check 'entry_point points at nothing' 1 "$d"
has 'point at nothing'

# --- the parser refuses rather than guessing ------------------------------------

d=$(catalog unparseable)
front "$d" 'type: luma/catalog
namespace: acme
superseded_by: [[ADR-0012]]'
check 'unquoted wikilink refused' 1 "$d"
has 'could not run'
has 'quote it'

d=$(catalog tabbed)
printf -- '---\ntype: luma/catalog\nnamespace: acme\nstarters:\n\tproject: x\n---\n' > "$d/catalog.md"
check 'tab indentation refused' 1 "$d"
has 'tabs'

# A broken catalog.md must skip the other checks rather than reporting nonsense.
lacks 'both mandated'

# --- one check at a time ---------------------------------------------------------

d=$(catalog only)
front "$d" 'type: luma/catalog
requires:
  - bundle: acme/gone
    obligation: mandatory'
check 'only manifest' 1 "$d" --only manifest
has 'no namespace'
lacks 'does not publish'

check 'unknown check name' 2 "$d" --only nope
has 'unknown check'

# --- json -------------------------------------------------------------------------

check 'json findings' 1 "$d" --json
has '"check": "manifest"'
has '"severity"'

# --- the doctor never fails --------------------------------------------------------

good2=$(catalog doctor)
report 'report on a good catalog' 0 "$good2"
has 'widgets'
has 'preload'

# It reports on a catalog that check refuses, because it is not a gate.
d=$(catalog doctorbad)
front "$d" 'type: luma/catalog
requires:
  - bundle: acme/gone
    obligation: mandatory'
report 'report ignores findings' 0 "$d"

# ...but not on one it cannot read.
d=$(catalog doctorunparseable)
front "$d" 'type: luma/catalog
x: [[y]]'
report 'report on unreadable catalog' 2 "$d"

report 'report json' 0 "$good2" --json
has '"preload_words"'
has '"bundles": 1'

# --- --against: what changed without saying so -------------------------------------
#
# The only check that needs two trees, so these cases build a real repository
# rather than a directory. Still hermetic: git init under the temp directory,
# identity supplied per-command so no ambient config is read or written.

git() { command git -c user.name=t -c user.email=t@example.com -c commit.gpgsign=false "$@"; }

# gitcatalog <name> — a catalog committed in its own repository, under
# <repo>/catalog. Echoes the repository root.
gitcatalog() {
  r=$T/repo-$1
  c=$(catalog "src-$1")
  mkdir -p "$r" && mv "$c" "$r/catalog"
  git -C "$r" init -q >/dev/null 2>&1
  git -C "$r" add -A >/dev/null 2>&1
  git -C "$r" commit -qm base >/dev/null 2>&1
  printf '%s' "$r"
}

# Nothing changed, so nothing owes a version.
r=$(gitcatalog quiet)
check 'unchanged tree is quiet' 0 "$r" --against HEAD
has 'from 3 check(s)'
lacks 'without a version change'

# Without --against, git is never consulted and the check does not exist.
check 'no ref, no versioning check' 0 "$r"
has 'from 2 check(s)'
lacks 'versioning'

# The case this exists for: a bundle's files moved and its version did not.
r=$(gitcatalog stale)
printf 'Different rules entirely.\n' >> "$r/catalog/bundles/widgets/policy/rules.md"
check 'changed without a version change' 1 "$r" --against HEAD
has 'without a version change'
has 'widgets'
has 'still 0.1.0'

# Same edit, version moved. This is the half that has to stay quiet — a false
# positive in something wired pre-merge gets the check switched off.
printf -- '---\ntype: bundle\nversion: 0.1.1\nentry_point: workflows/make-a-widget\ndescription: Widgets.\n---\n' \
  > "$r/catalog/bundles/widgets/bundle.md"
check 'changed with a version change' 0 "$r" --against HEAD
lacks 'without a version change'

# Editing bundle.md itself without moving the number is still a change.
r=$(gitcatalog manifestonly)
printf -- '---\ntype: bundle\nversion: 0.1.0\nentry_point: workflows/make-a-widget\ndescription: Widgets, described differently.\n---\n' \
  > "$r/catalog/bundles/widgets/bundle.md"
check 'bundle.md edited, version standing still' 1 "$r" --against HEAD
has 'without a version change'

# An untracked file is a change to that bundle. A pre-merge job never sees one,
# but the author at a terminal does, and reporting clean there would be a lie.
r=$(gitcatalog untracked)
printf -- '---\ntype: policy\ntitle: More\ndescription: More rules.\n---\nWords.\n' \
  > "$r/catalog/bundles/widgets/policy/more.md"
check 'untracked file counts' 1 "$r" --against HEAD
has 'without a version change'

# A bundle that did not exist at the ref is new, and a new bundle owes no bump.
r=$(gitcatalog newbundle)
mkdir -p "$r/catalog/bundles/gadgets"
printf -- '---\ntype: bundle\nversion: 0.1.0\ndescription: Gadgets.\n---\n' \
  > "$r/catalog/bundles/gadgets/bundle.md"
check 'a new bundle owes no bump' 0 "$r" --against HEAD
lacks 'without a version change'

# A change outside every bundle is not a bundle's to account for.
r=$(gitcatalog manifestchange)
printf '\nProse under the manifest.\n' >> "$r/catalog/catalog.md"
check 'catalog.md is not a bundle' 0 "$r" --against HEAD
lacks 'without a version change'

# Two bundles, one stale: the finding names the one that moved.
r=$(gitcatalog twobundles)
mkdir -p "$r/catalog/bundles/gadgets"
printf -- '---\ntype: bundle\nversion: 0.1.0\ndescription: Gadgets.\n---\n' \
  > "$r/catalog/bundles/gadgets/bundle.md"
git -C "$r" add -A >/dev/null 2>&1
git -C "$r" commit -qm gadgets >/dev/null 2>&1
printf 'More.\n' >> "$r/catalog/bundles/gadgets/bundle.md"
check 'only the bundle that changed' 1 "$r" --against HEAD
has 'gadgets'
lacks 'widgets:'

# A manifest that did not parse at the ref cannot be compared, and says so
# rather than reporting either answer.
r=$(gitcatalog wasbroken)
printf -- '---\ntype: bundle\nversion: 0.1.0\nsee: [[nope]]\ndescription: x\n---\n' \
  > "$r/catalog/bundles/widgets/bundle.md"
git -C "$r" add -A >/dev/null 2>&1
git -C "$r" commit -qm broken >/dev/null 2>&1
printf -- '---\ntype: bundle\nversion: 0.1.0\ndescription: Widgets.\n---\n' \
  > "$r/catalog/bundles/widgets/bundle.md"
check 'unparseable at the ref' 1 "$r" --against HEAD
has 'could not be compared'

# A ref that does not exist is a failure, never a pass. This is the one that
# decides whether a misconfigured pre-merge job is green or red.
r=$(gitcatalog badref)
check 'unknown ref fails' 1 "$r" --against no-such-branch
has 'could not compare'
has 'no such commit'

# --- tier honesty: surfaced, never refused -------------------------------------
#
# These are notices. A heuristic wired to a merge gate is a heuristic that gets
# switched off, so every case below must exit 0 while still saying something.

bump() {
  printf -- '---\ntype: bundle\nversion: %s\nentry_point: workflows/make-a-widget\ndescription: Widgets.\n---\n' \
    "$2" > "$1/catalog/bundles/widgets/bundle.md"
}

# A patch that edits a `must` is the dangerous tier: two characters, the diff of
# a typo, a complete reversal.
r=$(gitcatalog normative)
printf 'A widget must not be blue.\n' >> "$r/catalog/bundles/widgets/policy/rules.md"
bump "$r" 0.1.1
check 'patch touching a normative sentence' 0 "$r" --against HEAD
has 'NOTICE'
has 'normative sentence'
has 'must not be blue'
has 'never fails a run'

# The same edit as a minor is the author saying behaviour changed. No notice.
r=$(gitcatalog normativeminor)
printf 'A widget must not be blue.\n' >> "$r/catalog/bundles/widgets/policy/rules.md"
bump "$r" 0.2.0
check 'minor touching a normative sentence' 0 "$r" --against HEAD
lacks 'normative sentence'

# Ordinary prose on a patch stays quiet — the false-positive half.
r=$(gitcatalog ordinary)
printf 'Widgets are usually round.\n' >> "$r/catalog/bundles/widgets/policy/rules.md"
bump "$r" 0.1.1
check 'patch touching ordinary prose' 0 "$r" --against HEAD
lacks 'normative sentence'

# Removing a document in a non-major release is a signal, not a verdict.
r=$(gitcatalog removal)
rm "$r/catalog/bundles/widgets/policy/rules.md"
bump "$r" 0.2.0
check 'minor removing a document' 0 "$r" --against HEAD
has 'removed a document'
has 'rules.md'

# In a major, removal is what major is for. Nothing to say.
r=$(gitcatalog majorremoval)
rm "$r/catalog/bundles/widgets/policy/rules.md"
bump "$r" 1.0.0
check 'major removing a document' 0 "$r" --against HEAD
lacks 'removed a document'

# A version scheme the comparator does not understand must not be guessed at.
r=$(gitcatalog oddscheme)
printf 'A widget must not be blue.\n' >> "$r/catalog/bundles/widgets/policy/rules.md"
bump "$r" 2026-08-23
check 'unfamiliar version scheme is not judged' 0 "$r" --against HEAD
lacks 'normative sentence'

# A notice alone never changes the exit code, even alongside a real finding.
r=$(gitcatalog both)
printf 'A widget must not be blue.\n' >> "$r/catalog/bundles/widgets/policy/rules.md"
bump "$r" 0.1.1
check 'notice alone exits 0' 0 "$r" --against HEAD
has '0 finding(s) and 1 notice(s)'

# ...and so is a catalog that is not in a repository at all.
d=$(catalog notarepo)
check 'not a git repository' 1 "$d" --against HEAD
has 'could not compare'

# --only versioning without a ref would run nothing and report zero findings.
r=$(gitcatalog onlyref)
check 'versioning needs a ref' 2 "$r" --only versioning
has 'needs --against'

printf 'Changed.\n' >> "$r/catalog/bundles/widgets/policy/rules.md"
check 'only versioning' 1 "$r" --only versioning --against HEAD
has 'check=versioning'
has 'from 1 check(s)'

check 'versioning json' 1 "$r" --only versioning --against HEAD --json
has '"check": "versioning"'

printf '\n%d passed, %d failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ] || exit 1
