---
type: policy
title: The estate, and what each repository owns
description: The six repositories, the boundary each one defends, and the rule that decides where a new thing goes. Read before adding anything to any of them.
applies_to:
  - topic: deciding which repository a new thing belongs in
---

# The estate, and what each repository owns

**Six repositories, and the boundaries are load-bearing rather than tidy.** Most
mistakes here are a thing landing in the wrong one, which is cheap to fix on the
day and expensive later.

| | what it is | owns |
| --- | --- | --- |
| **`luma-knowledge-format`** | the specification | documents, bundles, types. **Nothing about distribution** |
| **`luma-catalog`** | the universal catalog | published bundles. **No executable code** |
| **`luma-leader`** | the organization's headquarters | decisions, design drafts, cross-project reasoning |
| **`luma-foreman`** | the project-side engine | adoption, projection, inspection |
| **`luma-clarify`** | ambiguity in written requirements | its own domain entirely |
| **`luma-backlog`** | intended work | its own domain entirely |

## Projects split on runtime location, not on subject matter

**That is the rule, and it is why the split looks odd from the outside.**
`foreman` and `curator` both concern bundles and belong in different
repositories, because one runs where bundles are *adopted* and the other where
they are *published* — different repositories, different people, different
release cadences.

Asking *what is this about* produces the wrong answer every time. Ask **where
does it run**.

## The three boundaries most often crossed by accident

**The format must not learn about our distribution model.** It defines the
Bundle because its own machinery needs one — a Document ID is a path within a
Bundle, and types resolve from a Bundle's `_types/`. It knows nothing of
catalogs, adoption or projects, and a change that would teach it any of those is
in the wrong repository.

**A built-in type takes a word from everyone, permanently.** The bar is not
importance: *"a consumer that ignored it would be broken"* means broken as a
reader of the format, not broken as a user of our tools. `luma/project` and
`luma/catalog` both failed that bar and live in the `luma/luma-types` bundle
instead. **Importance is what a namespace is for.**

**The catalog holds no executable code.** A catalog is copied from by agents, and
code arriving that way is a way for things to go wrong that nobody is watching
for. Tooling that checks or adopts bundles lives in an engine.

## Naming anything new

**Name a tool for the verb it performs**, as an agent noun — the
`compiler`/`linker` shape. The test is whether somebody who has read nothing can
guess what it does.

**The corollary is the useful half.** If the job cannot be stated as one verb,
that is a signal about the tool rather than about the name — a name that has to
be a metaphor usually means more than one job is hiding behind it. `foreman`
inspects, bootstraps, outfits and refits, which is four verbs and exactly why it
needed a metaphor. **The rule doubles as a junk-drawer detector.**

`leader` and `foreman` keep their names. A convention that requires renaming
everything before it can be adopted is one nobody adopts.

**Two suffixes are reserved.** `-hq` means an organization's own headquarters and
nothing else ever; `<org>-catalog` is a catalog rather than an engine. Both exist
because a near-collision already misled a fresh agent once.

## Everything is committed, and deletion is not the tool

**Records are append-only, decisions are archived rather than deleted, and the
history is the safety net.** That is what makes it safe to move fast: any state
is recoverable, so a wrong turn costs a revert rather than a reconstruction.

**It is also what makes the estate measurable.** Reconstructing *what was in
force on a given date* is possible only because archived decisions keep their
dates and their reasoning — a property that was not designed for measurement and
turns out to enable it.

## A repository does not vendor its own bundles into itself

**Reference within a repository; vendor across them.** A catalog already
*contains* the bundles it publishes, so adopting them puts two byte-identical
trees in one repository with nothing keeping them in step — and the drift check
cannot help, because it catches an *edited* copy rather than an *outdated* one.

**The cost is real and is accepted.** An agent working in a catalog gets no
generated index and no skills, because `outfit` projects what a project
*adopted* and a catalog adopted nothing. It has to be pointed at
`catalog/bundles/` by hand.

**Projecting what a repository publishes is the missing feature**, and it is not
as simple as it looks: this catalog publishes seventeen bundles and works by
about three, so projecting all of them would be a worse problem than the
duplication it replaced. What is missing is the adopter's own selection — the
same question `preload_default` answers for adopted bundles — and inventing it
in passing would be worse than the gap.

## You are also an ordinary user

**A maintainer runs the tools the same way anybody does**, and the moment a tool
grows a path that only works here, the separation has failed. The test is
mechanical: **an engine should contain no knowledge of `luma` specifically.** If
one does, it is deciding policies rather than enforcing them.
