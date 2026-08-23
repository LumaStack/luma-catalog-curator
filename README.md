# luma-catalog-curator

> **Tends a catalog.**<br>
> Validates what it holds, refuses what it cannot hold consistently, and reports what it is becoming.

> **Status:** early. The checks that need bundle dependencies are absent because nothing has dependencies yet.

**Anyone runs one.** This is not a luma maintainers' script — an organization with its own catalog needs the same checks over the same shapes, and it contains no knowledge of any particular catalog. If it ever grows a check that only makes sense here, that is a bug.

```bash
luma-catalog-curator check ../acme-catalog            # 0 clean, 1 findings, 2 could not run
luma-catalog-curator check --against origin/main .    # ...and what changed without saying so
luma-catalog-curator report ../acme-catalog           # what the catalog is becoming
```

## Gate or report is decided by the wiring, not by the tool

`check` returns an exit code, so a pre-merge job makes it a gate and a person at a terminal makes it a report. The design document treats this as an either/or that has to be settled first; it does not, and settling it in the tool would be the tool deciding somebody else's process.

What the tool does decide is that **an unenforced check is decoration** — so `check` is built to be wired, and `report` is built never to fail.

**`luma-catalog` wires it as a gate**: a required pre-merge job runs `check`, `check --against origin/main` and `luma-foreman inspect`, and branch protection means a red run blocks the merge. That is one catalog's configuration rather than this tool's opinion, and it is the worked example to copy.

## `--against <ref>` — the check that needs two trees

Everything else here is answerable from the catalog on disk. **Whether a version is honest is not**: a version means nothing except relative to what the same bundle used to be, so that check runs only when you name something to compare with.

```bash
luma-catalog-curator check --against origin/main .
```

It reports **any bundle whose files changed while the `version` in its `bundle.md` did not**. An adopter decides whether to take a change by comparing versions, so a change that does not move the number is a change nobody downstream can see — and diffing a directory they did not write is their only alternative.

**It does not judge the tier — it points at two signals and lets you judge.** Major, minor or patch stays the author's call. But two things are mechanical to spot and worth a second reader, so both are reported as **notices**, which print as loudly as a finding and never fail a run:

- **A patch that edits a normative sentence.** `must not` → `must` is two characters, the diff of a typo, and a complete reversal — and *"patch: fixed wording"* gets approved in seconds. The check cannot know whether the meaning changed; it can know the edit landed where meaning lives.
- **A non-major release that removes a document.** Subtraction signals major and is not a rule: removing a carve-out is also how prose gets stronger.

*Surface, never refuse* is what the version design asks for, and it is why these cannot fail a build. **A heuristic wired to a merge gate is a heuristic that gets switched off.**

- **A bundle that did not exist at the ref is new**, and owes no bump.
- **Untracked files count.** A pre-merge job never sees one, but the author at a terminal does, and reporting clean there would be a lie.
- **A ref that will not resolve is a finding, not a skip.** A misconfigured pre-merge job goes red rather than green, because a comparison that could not be made is not a comparison that found nothing.

Without `--against`, nothing here reads git at all.

**Its subject is one bundle, which looks like foreman's half of the line — and is not.** The split this estate draws is runtime location: a check belongs here if it can only run where a catalog is *written*. This one needs the catalog's history, which an adopter does not have and foreman never sees. The rule *one bundle in isolation is foreman's* holds; a bundle against its own past is not in isolation.

## What it checks, and what it deliberately does not

**It checks a *set*.** Every check here is meaningless about one bundle in isolation:

- a bundle both **mandated and deprecated** — not a precedence puzzle, a broken catalog
- a **starter pinning a version the catalog's own mandate forbids**, which would make every new consumer born failing
- **requirements and starters naming bundles the catalog does not publish**
- **requirement tags outside the published vocabulary**, which never fire and report green while doing it
- **no namespace declared**, so nothing can address what the catalog publishes
- bundles with no version, no description, or an `entry_point` pointing at nothing

**It does not check whether a bundle is internally sound.** A dangling wikilink, an unquoted frontmatter wikilink, a template carrying live frontmatter — those are properties of one bundle, need no catalog to find, and `luma-foreman inspect` already reports them. Run both.

That overlap is a known open question. The recorded position is *no shared package until two real consumers exist*, so the duplication is allowed to happen first and gets extracted once the shape is known.

**It will never know an organization's conventions.** Which directories a bundle uses, how workflows are named, when something may call itself `1.0.0` — those are opinions that arrive by adoption. A tool that compiled them in would be deciding standards rather than checking them, and would be useless to the second organization that ran it.

**It never adopts anything.** That is foreman's, and a curator that also adopted would have collapsed the split it exists to express.

## `report` — the doctor

Individual entries are defensible and the aggregate is what nobody sees.

```
luma — 17 bundle(s), 77 document(s)

bundle                      version  docs  preload   words
----------------------------------------------------------
session-manager               0.2.0     9        2    3422
bundle-manager                0.2.1     9        2    3097
...
----------------------------------------------------------
every bundle adopted                                 25174
```

**The last column is the number this tool exists to produce.** It is what a bundle costs an adopter in *every session*, unconditionally — the sum of its `preload: mandatory` documents. **A catalog can compute it and an adopter cannot see it before adopting**, which is exactly the asymmetry a publisher-side tool is for.

No package manager reports this, because no package manager has a context budget to spend.

## Reading YAML without a dependency

`catalog.md` holds nested maps and lists of maps, so the flat `key: value` subset foreman uses cannot read it. This carries its own reader, and **it refuses rather than guesses.**

The estate already has three partial frontmatter parsers and nothing that makes them agree. The danger is not the count — it is that a partial parser *silently produces a wrong answer* for input it half-understands, so two tools reach opposite conclusions about one file and nothing surfaces that they read different grammars.

**A reader that raises on anything outside its grammar cannot join that argument.** Tabs, anchors, aliases, block scalars, flow mappings, a second document, and an unquoted `[[…]]` are all refused by name. It is a weaker guarantee than a conformance suite and it is the one available without adding a dependency.

## Install

Requires Python 3.11+. No build step, no dependencies.

```bash
git clone https://github.com/LumaStack/luma-catalog-curator.git
ln -s "$PWD/luma-catalog-curator/bin/luma-catalog-curator" ~/.local/bin/
```

**There are no releases and no tags**, so a clone tracks `main`. That is a real limitation shared with every tool in this estate rather than a preference.

Run the tests with `sh tests/run`. They are hermetic — every case builds a throwaway catalog under a temp directory, and the `--against` cases build a throwaway git repository. They run on every pull request here, on the oldest and newest supported Python.

## What blocks the rest of it

**Publication is an event in `luma-catalog`, and nowhere else by default.** *Reject at publication* had no moment to attach to; it has one now — merging to that catalog's `main` is publication, and a required pre-merge job runs these checks before it. **Any other catalog is unwired**, and this tool cannot wire one: the enforcement is a repository's configuration, and a tool that gated a catalog it was merely pointed at would be deciding somebody else's process. That is the cost of *anyone runs one*, and `luma/luma-maintainers`' publish workflow is the copyable example.

**Nothing has dependencies.** Roughly half the designed checks — joint satisfiability, requiring a reason for a narrow constraint, cross-bundle links at resolved versions — have nothing to check. They are absent rather than stubbed.

The full design, including what was considered and rejected, is `luma-leader/docs/curator.md`.
