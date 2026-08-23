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

printf '\n%d passed, %d failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ] || exit 1
