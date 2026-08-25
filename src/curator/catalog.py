"""A catalog on disk, read once so every check sees the same thing.

**Reading is separate from checking on purpose.** A malformed manifest is one
finding, not one per check that tripped over it — and a check that has to guess
whether the thing it was handed parsed is a check that will report nonsense when
the answer is no.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from . import yamlish

# `_types/` holds contracts and `templates/` holds assets carrying fenced
# examples. Neither is content a consumer loads, so neither counts toward what a
# bundle costs to adopt.
NOT_CONTENT = ("_types", "templates")


@dataclass(frozen=True)
class Doc:
    """A Document inside a bundle."""

    doc_id: str
    path: Path
    type: str
    title: str
    description: str
    preload: str
    words: int


@dataclass(frozen=True)
class Bundle:
    """One bundle a catalog publishes."""

    name: str
    root: Path
    manifest: dict
    docs: tuple[Doc, ...]
    error: str | None = None

    @property
    def version(self) -> str:
        return str(self.manifest.get("version", ""))

    @property
    def description(self) -> str:
        return str(self.manifest.get("description", ""))

    @property
    def entry_point(self) -> str:
        return str(self.manifest.get("entry_point", ""))

    def preload_words(self) -> int:
        """What adopting this costs an adopter in every session, unconditionally."""
        return sum(d.words for d in self.docs if d.preload == "mandatory")


@dataclass
class Catalog:
    """A catalog's content directory, its manifest, and its bundles.

    **Two ways of not working, and conflating them is how a checker lies.**
    `missing` means there is no catalog here — a usage error, and the tool
    could not run. `error` means there *is* one and it is broken — a defect in
    the catalog, which is a finding and must fail.
    """

    root: Path
    manifest: dict = field(default_factory=dict)
    bundles: list[Bundle] = field(default_factory=list)
    error: str | None = None
    missing: bool = False

    @property
    def namespace(self) -> str:
        return str(self.manifest.get("namespace", ""))

    @property
    def tags(self) -> list[str]:
        value = self.manifest.get("tags", [])
        return [str(t) for t in value] if isinstance(value, list) else []

    @property
    def requires(self) -> list[dict]:
        value = self.manifest.get("requires", [])
        return [r for r in value if isinstance(r, dict)] if isinstance(value, list) else []

    @property
    def starters(self) -> dict:
        value = self.manifest.get("starters", {})
        return value if isinstance(value, dict) else {}

    def names(self) -> set[str]:
        """Bundle IDs this catalog publishes, namespaced when it declares one."""
        prefix = f"{self.namespace}/" if self.namespace else ""
        return {f"{prefix}{b.name}" for b in self.bundles}

    def publishes(self, bundle_id: str) -> bool:
        if bundle_id in self.names():
            return True
        # An unqualified name is this catalog's own by convention.
        return "/" not in bundle_id and any(b.name == bundle_id for b in self.bundles)


def find(start: Path) -> Path | None:
    """A catalog's content directory — where `CATALOG.md` sits.

    Checked one level down as well, because a catalog repository conventionally
    keeps its content under `catalog/` and pointing a tool at the repository is
    what anybody would do.
    """
    for candidate in (start, start / "catalog"):
        if (candidate / "CATALOG.md").is_file():
            return candidate
    return None


def _read(path: Path) -> tuple[dict | None, str | None]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return None, str(exc)
    try:
        return yamlish.frontmatter(text), None
    except yamlish.YamlishError as exc:
        return None, str(exc)


# `README.md` is deliberately never an owner, whatever it contains. It carries
# universal permission semantics — everybody believes they may edit it freely —
# so a system depending on its structure has a fuse in it.
NEVER_OWNS = ("README",)


def _owns_directory(path: Path) -> bool:
    """Is this the all-caps Document that its directory *is*?

    The casing is the signal rather than any particular word, so a workflow gets
    `WORKFLOW.md` and somebody's own type gets its own — nothing is centrally
    reserved, which the open type vocabulary requires.
    """
    return path.stem.isupper() and path.stem not in NEVER_OWNS


def _docs(root: Path) -> list[Doc]:
    # A directory that *is* a Document owns everything beneath it: a tutorial's
    # steps are reachable only through the tutorial and never listed
    # separately. The bundle's own manifest owns the bundle root by the same
    # rule and must not hide it — subordination applies within a bundle, never
    # at its root, because a bundle's members are its content.
    owned = {
        path.parent
        for path in root.rglob("*.md")
        if path.parent != root and _owns_directory(path)
    }

    out: list[Doc] = []
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        if rel.parts[0] in NOT_CONTENT or rel.as_posix() == "BUNDLE.md":
            continue
        if any(parent in owned for parent in path.parents if parent != path.parent or not _owns_directory(path)):
            continue
        front, error = _read(path)
        if front is None or error or "type" not in front:
            continue
        body = path.read_text(encoding="utf-8").split("\n---", 1)[-1]
        out.append(
            Doc(
                # The directory is the identity. `WORKFLOW.md` is a local
                # detail nothing references, so the ID shortens to the
                # directory that holds it.
                doc_id=(rel.parent.as_posix() if _owns_directory(path)
                        else rel.as_posix()[:-3]),
                path=path,
                type=str(front.get("type", "")),
                title=str(front.get("title", "")),
                description=str(front.get("description", "")),
                preload=str(front.get("preload", "") or "optional"),
                words=len(body.split()),
            )
        )
    return out


def load(start: Path) -> Catalog:
    root = find(start)
    if root is None:
        return Catalog(
            root=start,
            missing=True,
            error=f"no catalog here — nothing named CATALOG.md in {start} or {start}/catalog",
        )

    manifest, error = _read(root / "CATALOG.md")
    catalog = Catalog(root=root, manifest=manifest or {})
    if error:
        catalog.error = f"CATALOG.md: {error}"
        return catalog
    if manifest is None:
        catalog.error = "CATALOG.md has no frontmatter, so it declares nothing"
        return catalog

    directory = root / "bundles"
    if not directory.is_dir():
        return catalog

    for entry in sorted(p for p in directory.iterdir() if p.is_dir()):
        bundle_manifest = entry / "BUNDLE.md"
        if not bundle_manifest.is_file():
            continue
        front, err = _read(bundle_manifest)
        catalog.bundles.append(
            Bundle(
                name=entry.name,
                root=entry,
                manifest=front or {},
                docs=tuple(_docs(entry)),
                error=f"BUNDLE.md: {err}" if err else None,
            )
        )
    return catalog
