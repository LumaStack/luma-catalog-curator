"""Block YAML, for the shapes a catalog manifest actually uses.

**A subset that refuses rather than guesses, and the refusing is the point.**

The estate already has three partial frontmatter parsers and nothing that makes
them agree. The danger in that is not the count — it is that a partial parser
**silently produces a wrong answer** for input it half-understands. Foreman's
reader treats an unquoted wikilink as a defect; a real YAML parser reads it as a
nested array; both behave correctly and reach opposite conclusions, and nothing
surfaces that they read different grammars.

**This one cannot join that argument, because it raises on anything outside its
grammar.** A fourth reader that fails loudly cannot disagree quietly with the
other three. That is a weaker guarantee than a conformance suite and it is the
one available without adding a dependency to a tool that promises none.

What it reads:

- `key: value` mappings, nested by indentation
- `- item` sequences, of scalars or of mappings
- `[a, b, c]` flow sequences of scalars
- `#` comments, blank lines, single and double quoted scalars

What it refuses **by name** rather than mis-reading: tabs, anchors, aliases,
tags, block scalars, flow mappings, a second document, and an unquoted value
beginning `[[` — which is a nested sequence to YAML and a wikilink to a person.

**Everything comes back as a string, a list, or a dict.** No coercion: a version
is `"0.2.0"` whether or not somebody quoted it, and `no` stays the word rather
than becoming `False`. Coercion is where YAML's real surprises live, and a tool
that only compares and reports has no use for it.
"""

from __future__ import annotations

import re

FLOW = re.compile(r"^\[(.*)\]$")
KEY = re.compile(r"^([A-Za-z_][\w.-]*)\s*:(?:\s+(.*))?$")

Row = tuple[int, int, str]  # line number, indent, content


class YamlishError(ValueError):
    """Input outside the supported grammar. Never raised for valid subset input."""

    def __init__(self, line: int, message: str) -> None:
        super().__init__(f"line {line}: {message}")
        self.line = line


# --------------------------------------------------------------------------
# scalars


def _unquote(text: str) -> str:
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        return text[1:-1]
    return text


def _scalar(raw: str, line: int) -> str | list[str]:
    text = raw.strip()
    if not text:
        return ""
    if text[0] in "&*!":
        kind = {"&": "an anchor", "*": "an alias", "!": "a tag"}[text[0]]
        raise YamlishError(line, f"{kind} is not supported")
    if text[0] in "|>":
        raise YamlishError(line, "block scalars are not supported")
    if text.startswith("{"):
        raise YamlishError(line, "flow mappings are not supported")
    if text.startswith("[["):
        raise YamlishError(
            line,
            "unquoted [[...]] is a nested sequence to YAML and a wikilink to a "
            "person — quote it",
        )

    flow = FLOW.match(text)
    if flow:
        inner = flow.group(1).strip()
        if not inner:
            return []
        if "[" in inner or "]" in inner:
            raise YamlishError(line, "nested flow sequences are not supported")
        return [_unquote(p.strip()) for p in inner.split(",")]

    return _unquote(text)


# --------------------------------------------------------------------------
# rows


def _rows(text: str) -> list[Row]:
    out: list[Row] = []
    for n, raw in enumerate(text.split("\n"), start=1):
        lead = raw[: len(raw) - len(raw.lstrip())]
        if "\t" in lead:
            raise YamlishError(n, "tabs are not valid YAML indentation")
        content = raw.strip()
        if not content or content.startswith("#"):
            continue
        if content in ("---", "..."):
            raise YamlishError(n, "multiple documents are not supported")
        out.append((n, len(raw) - len(raw.lstrip(" ")), content))
    return out


# --------------------------------------------------------------------------
# the grammar


def _block(rows: list[Row], i: int, indent: int):
    if rows[i][2] == "-" or rows[i][2].startswith("- "):
        return _sequence(rows, i, indent)
    return _mapping(rows, i, indent)


def _nested(rows: list[Row], i: int, indent: int):
    """The block belonging to a key that had no inline value."""
    if i >= len(rows) or rows[i][1] <= indent:
        return "", i
    return _block(rows, i, rows[i][1])


def _mapping(rows: list[Row], i: int, indent: int) -> tuple[dict, int]:
    out: dict = {}
    while i < len(rows):
        line, level, content = rows[i]
        if level < indent:
            break
        if level > indent:
            raise YamlishError(line, "unexpected indentation in a mapping")
        if content == "-" or content.startswith("- "):
            break
        match = KEY.match(content)
        if not match:
            raise YamlishError(line, f"expected `key: value`, got {content!r}")
        key, raw = match.group(1), match.group(2)
        if key in out:
            raise YamlishError(line, f"duplicate key: {key}")
        i += 1
        if raw is None or not raw.strip():
            out[key], i = _nested(rows, i, indent)
        else:
            out[key] = _scalar(raw, line)
    return out, i


def _sequence(rows: list[Row], i: int, indent: int) -> tuple[list, int]:
    items: list = []
    while i < len(rows):
        line, level, content = rows[i]
        if level < indent:
            break
        if level > indent:
            raise YamlishError(line, "unexpected indentation in a sequence")
        if content == "-":
            raise YamlishError(line, "an empty sequence entry is not supported")
        if not content.startswith("- "):
            break

        rest = content[2:].strip()
        match = KEY.match(rest)
        if match and not rest.startswith("[["):
            # `- key: value` — an inline mapping whose remaining keys sit at the
            # column where this first key began. Re-present it as an ordinary
            # mapping at that indent rather than special-casing the parse.
            inner = indent + 2
            rewritten: list[Row] = [(line, inner, rest)]
            j = i + 1
            while j < len(rows) and rows[j][1] >= inner and not (
                rows[j][1] == inner and rows[j][2].startswith("- ")
            ):
                rewritten.append(rows[j])
                j += 1
            entry, consumed = _mapping(rewritten, 0, inner)
            if consumed != len(rewritten):
                raise YamlishError(rewritten[consumed][0], "unexpected indentation")
            items.append(entry)
            i = j
        else:
            items.append(_scalar(rest, line))
            i += 1
    return items, i


# --------------------------------------------------------------------------
# entry points


def loads(text: str) -> dict:
    """Parse a block-YAML mapping. Raises YamlishError outside the subset."""
    rows = _rows(text)
    if not rows:
        return {}
    value, i = _block(rows, 0, rows[0][1])
    if i != len(rows):
        raise YamlishError(rows[i][0], "unexpected indentation")
    if not isinstance(value, dict):
        raise YamlishError(rows[0][0], "expected a mapping at the top level")
    return value


def frontmatter(text: str) -> dict | None:
    """A Document's frontmatter, or None when it has none.

    None means *this is an Asset* — a file with no frontmatter — which a Bundle
    may legitimately contain and which is never an error.
    """
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    return loads(text[4:end])
