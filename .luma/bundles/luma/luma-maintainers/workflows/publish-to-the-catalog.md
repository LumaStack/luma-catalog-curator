---
type: workflow
title: Publish a bundle to the universal catalog
description: Add or change a bundle in luma-catalog and get the version honest. Use when promoting something out of a project, or changing anything already published.
---

# Publish a bundle to the universal catalog

**Publishing is a commitment, and that is the part worth slowing down for.** A
project bundle is a draft. A catalog entry is a surface other people build on,
and changing its shape stops being free the moment somebody adopts it.

## 1. Has it earned a place here?

**Two triggers, either one is enough:** several projects are already using it —
the copies are real rather than anticipated — or it is foundational, the thing
other content leans on.

**The cost of being wrong is asymmetric.** Promoting late costs a duplicated copy
or two: visible, annoying, fixable. Promoting early costs every adopter who built
on a shape that had not settled, which is none of those things.

**Two copies are a signal, not yet a problem.** It is usually the third that says
a thing is genuinely shared rather than coincidentally similar.

**The exemption:** something built explicitly to be shared does not have to prove
itself through three projects first.

## 2. Get the version honest

**Size carries no signal.** Delete one word: if the word is *the*, nothing
changed; if the word is *not*, everything did. The unit is the **normative
claim** — what did this require, permit or forbid before, and what does it now.

| | test |
| --- | --- |
| **major** | **an adopter has to do something on their side** to keep getting the result they had |
| **minor** | more, or sharper. A reader's expectations still hold |
| **patch** | **could not change what anyone does** |

**Patch is the dangerous tier here, and it inverts the code intuition.**
`must not` → `must` is two characters, the diff of a typo, and a complete
reversal. **A patch does not touch a normative sentence** — if the edit lands on
a *must*, *never*, *always*, a threshold or a condition, it is not a patch
however few characters moved.

**Removals are a flag, not a verdict.** Removing an exception somebody relied on
is major; removing a permissive option nobody had to use is minor; removing a
paragraph nobody acted on is patch. **One kind is objective and gets rejected
outright**: removing a document others link to, or a field from a type when
records exist against it.

## 3. Write the `## Version` section

**Newest first, with the reasoning.** This is what an adopter reads to decide
whether to take the change, so state what they have to do rather than only what
moved.

**Say what is provisional.** A section that admits what has not been tested is
worth more than one that reads as finished.

## 4. Audit before it goes

```bash
luma-foreman inspect
```

**The defects this catches are all silent ones.** A dangling wikilink, an
unquoted wikilink in frontmatter, a template carrying live frontmatter, a link
that escapes the bundle. Every one of them is conformant, so the bundle
publishes cleanly and the defect travels to every adopter.

**Wikilinks do not cross bundles.** A link into another bundle resolves to
nothing, because bundles are self-contained. Name the other bundle in prose
instead.

## 5. Check the catalog still agrees with itself

**Some contradictions only the catalog can see**, and no individual project ever
could: a bundle both mandated and deprecated, or a starter pinning a version the
same catalog's own mandate forbids — which would make every new project born
failing.

```bash
luma-catalog-curator check .
```

**This is the check no individual project could ever run**, which is why it
belongs here rather than in `foreman inspect`. It reads a *set*: whether these
declarations can all be true at once.

**It is not wired to anything.** Publication is still not an event — a bundle
becomes available by being committed to `main` — so nothing runs this unless
somebody does. An unenforced check is decoration, and this one currently is.

## 6. Merge, then let adopters find it

Merge commits rather than squash or rebase — the commit message is where the
rationale lives, and squashing discards it.

**Nothing notifies anybody.** Adopters find a newer version by running `adopt`
again, and no mechanism tells them to. That is a known hole rather than a
design.
