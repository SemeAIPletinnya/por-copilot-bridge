"""Proof-of-Resonance compatibility adapter.

This module intentionally maps local bridge states to a small PoR-shaped
payload without importing or depending on any external Silence-as-Control
package.
"""

from __future__ import annotations

from typing import Any

from .models import BridgeDecision, Decision


def to_por_state(decision: Decision) -> str:
    """Return the PoR-compatible state string for a bridge decision."""

    return decision.value


def result_to_por_payload(result: BridgeDecision) -> dict[str, Any]:
    """Return a deterministic PoR-compatible payload for a bridge result."""

    return {
        "por_state": result.decision.value,
        "decision": result.decision.value,
        "risk_level": result.risk_level.value,
        "reasons": list(result.reasons),
        "required_evidence": list(result.required_evidence),
        "control_layer": "por-copilot-bridge",
    }
