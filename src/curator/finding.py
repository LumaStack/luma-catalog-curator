"""What a check reports.

**Deliberately the same shape as foreman's, and deliberately a copy.** *No
shared package until two real consumers exist* is a settled position, and the
curator doc reaches the same conclusion for this specific overlap: *"let the
duplication happen first and extract when the shape is known."*

Two consumers now exist, so extraction has become arguable — and the shapes have
not yet been compared under load. The copy stays until one of them needs a field
the other does not, which is the evidence that would say what the shared thing
should be.

The distinction between a check that **ran and found nothing** and a check that
**could not run** is the reason `Skipped` exists alongside `Finding`. An
inspection reading clean while silently skipping half its checks manufactures
confidence nobody earned.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Ordered worst first, so sorting is this tuple's index.
SEVERITIES = ("high", "medium", "low")


@dataclass(frozen=True)
class Finding:
    check: str
    severity: str
    summary: str
    evidence: tuple[str, ...] = ()
    remedy: str = ""

    def __post_init__(self) -> None:
        if self.severity not in SEVERITIES:
            raise ValueError(f"unknown severity: {self.severity}")

    @property
    def rank(self) -> int:
        return SEVERITIES.index(self.severity)

    def as_dict(self) -> dict[str, object]:
        return {
            "check": self.check,
            "severity": self.severity,
            "summary": self.summary,
            "evidence": list(self.evidence),
            "remedy": self.remedy,
        }


@dataclass(frozen=True)
class Skipped:
    """A check that could not run, and why. Rendered as loudly as a finding."""

    check: str
    reason: str
    remedy: str = ""

    def as_dict(self) -> dict[str, object]:
        return {"check": self.check, "reason": self.reason, "remedy": self.remedy}


@dataclass
class Result:
    findings: list[Finding] = field(default_factory=list)
    skipped: list[Skipped] = field(default_factory=list)
    ran: list[str] = field(default_factory=list)

    def extend(self, other: "Result") -> None:
        self.findings.extend(other.findings)
        self.skipped.extend(other.skipped)
        self.ran.extend(other.ran)

    def sorted_findings(self) -> list[Finding]:
        return sorted(self.findings, key=lambda f: (f.rank, f.check, f.summary))
