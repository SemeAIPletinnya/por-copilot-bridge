"""Public bridge API."""

from __future__ import annotations

from .models import BridgeDecision, Proposal
from .risk_rules import evaluate_risk
from .router import route_decision


def evaluate_proposal(proposal: Proposal | dict) -> BridgeDecision:
    """Evaluate a coding-agent proposal and assign release-governance state."""

    normalized = Proposal.from_mapping(proposal) if isinstance(proposal, dict) else proposal
    findings = evaluate_risk(normalized)
    return route_decision(normalized, findings)
