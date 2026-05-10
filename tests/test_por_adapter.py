from por_copilot_bridge import (
    BridgeDecision,
    Decision,
    RiskLevel,
    result_to_por_payload,
    to_por_state,
)


def test_proceed_maps_to_por_state():
    assert to_por_state(Decision.PROCEED) == "PROCEED"


def test_needs_review_maps_to_por_state():
    assert to_por_state(Decision.NEEDS_REVIEW) == "NEEDS_REVIEW"


def test_silence_maps_to_por_state():
    assert to_por_state(Decision.SILENCE) == "SILENCE"


def test_result_to_por_payload_includes_compatibility_fields():
    result = BridgeDecision(
        decision=Decision.NEEDS_REVIEW,
        risk_level=RiskLevel.MEDIUM,
        reasons=("config mutation",),
        required_evidence=("configuration diff review",),
    )

    assert result_to_por_payload(result) == {
        "por_state": "NEEDS_REVIEW",
        "decision": "NEEDS_REVIEW",
        "risk_level": "medium",
        "reasons": ["config mutation"],
        "required_evidence": ["configuration diff review"],
        "control_layer": "por-copilot-bridge",
    }
