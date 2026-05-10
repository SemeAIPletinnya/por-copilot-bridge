"""Evidence helpers for deterministic proposal evaluation."""

from __future__ import annotations

from .models import EvidenceItem, Proposal

_VERIFICATION_TERMS = (
    "test passed",
    "tests passed",
    "verified",
    "verified works",
    "works locally",
    "validated",
)


def text_contains_verification_claim(text: str) -> bool:
    """Return True when text claims verification or passing tests."""

    lowered = text.lower()
    return any(term in lowered for term in _VERIFICATION_TERMS)


def has_verification_claim(proposal: Proposal) -> bool:
    """Return True if the proposal claims tests or verification succeeded."""

    fields = (proposal.title, proposal.body, *proposal.claims)
    return any(text_contains_verification_claim(field) for field in fields)


def has_passing_test_evidence(evidence: tuple[EvidenceItem, ...]) -> bool:
    """Return True only for explicit passing test/check evidence."""

    accepted_kinds = {"test", "tests", "check", "ci"}
    return any(item.passed and item.kind.lower() in accepted_kinds and item.detail for item in evidence)


def has_rollback_evidence(evidence: tuple[EvidenceItem, ...], proposal: Proposal) -> bool:
    """Return True if the proposal includes an explicit rollback note."""

    haystack = "\n".join([proposal.body, *proposal.claims, *(item.detail for item in evidence)]).lower()
    return "rollback" in haystack or "revert" in haystack
