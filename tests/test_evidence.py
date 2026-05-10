from por_copilot_bridge.evidence import has_passing_test_evidence, has_verification_claim
from por_copilot_bridge.models import EvidenceItem, Proposal


def test_verification_claim_detected_from_claims():
    proposal = Proposal(source="agent", title="Patch", claims=("verified works",))
    assert has_verification_claim(proposal)


def test_passing_test_evidence_requires_accepted_kind_and_detail():
    assert has_passing_test_evidence((EvidenceItem(kind="test", detail="pytest passed"),))
    assert not has_passing_test_evidence((EvidenceItem(kind="note", detail="looks good"),))
    assert not has_passing_test_evidence((EvidenceItem(kind="test", detail="pytest failed", passed=False),))
