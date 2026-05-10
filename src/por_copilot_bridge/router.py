"""Decision router that maps risk findings to release state."""

from __future__ import annotations

from .models import BridgeDecision, Decision, Proposal, RiskLevel
from .risk_rules import RuleFinding, is_comment_or_formatting_only, is_docs_only

_RISK_ORDER = {
    RiskLevel.LOW: 0,
    RiskLevel.MEDIUM: 1,
    RiskLevel.HIGH: 2,
    RiskLevel.CRITICAL: 3,
}


def route_decision(proposal: Proposal, findings: tuple[RuleFinding, ...]) -> BridgeDecision:
    """Assign explicit release state from deterministic findings."""

    if any(finding.silence for finding in findings):
        return _build(Decision.SILENCE, findings)

    if findings:
        return _build(Decision.NEEDS_REVIEW, findings)

    if is_docs_only(proposal.files_changed) or is_comment_or_formatting_only(proposal) or not proposal.files_changed:
        return BridgeDecision(
            decision=Decision.PROCEED,
            risk_level=RiskLevel.LOW,
            reasons=("safe release-governance path",),
            required_evidence=(),
        )

    return BridgeDecision(
        decision=Decision.NEEDS_REVIEW,
        risk_level=RiskLevel.MEDIUM,
        reasons=("unclassified executable or behavioral change",),
        required_evidence=("human review",),
    )


def _build(decision: Decision, findings: tuple[RuleFinding, ...]) -> BridgeDecision:
    risk_level = max((finding.risk_level for finding in findings), key=lambda item: _RISK_ORDER[item])
    reasons = tuple(dict.fromkeys(finding.reason for finding in findings))
    required = tuple(dict.fromkeys(finding.required_evidence for finding in findings if finding.required_evidence))
    return BridgeDecision(decision=decision, risk_level=risk_level, reasons=reasons, required_evidence=required)
