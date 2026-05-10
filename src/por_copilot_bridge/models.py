"""Data models for the deterministic release-governance bridge."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Decision(str, Enum):
    """Explicit release state assigned to a coding-agent proposal."""

    PROCEED = "PROCEED"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    SILENCE = "SILENCE"


class RiskLevel(str, Enum):
    """Bounded risk levels used by the bridge."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class EvidenceItem:
    """A deterministic evidence record supplied with a proposal."""

    kind: str
    detail: str
    passed: bool = True

    @classmethod
    def from_value(cls, value: Any) -> "EvidenceItem":
        if isinstance(value, EvidenceItem):
            return value
        if isinstance(value, dict):
            return cls(
                kind=str(value.get("kind", "note")),
                detail=str(value.get("detail", "")),
                passed=bool(value.get("passed", True)),
            )
        return cls(kind="note", detail=str(value), passed=True)


@dataclass(frozen=True)
class Proposal:
    """Coding-agent output candidate submitted for release governance."""

    source: str
    title: str
    body: str = ""
    files_changed: tuple[str, ...] = ()
    commands: tuple[str, ...] = ()
    claims: tuple[str, ...] = ()
    evidence: tuple[EvidenceItem, ...] = ()

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> "Proposal":
        return cls(
            source=str(data.get("source", "unknown")),
            title=str(data.get("title", "")),
            body=str(data.get("body", "")),
            files_changed=tuple(str(item) for item in data.get("files_changed", ())),
            commands=tuple(str(item) for item in data.get("commands", ())),
            claims=tuple(str(item) for item in data.get("claims", ())),
            evidence=tuple(EvidenceItem.from_value(item) for item in data.get("evidence", ())),
        )


@dataclass(frozen=True)
class BridgeDecision:
    """Release-governance result returned by the bridge."""

    decision: Decision
    risk_level: RiskLevel
    reasons: tuple[str, ...] = field(default_factory=tuple)
    required_evidence: tuple[str, ...] = field(default_factory=tuple)

    def as_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision.value,
            "risk_level": self.risk_level.value,
            "reasons": list(self.reasons),
            "required_evidence": list(self.required_evidence),
        }
