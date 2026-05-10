# Silence-as-Control integration

`silence-as-control` is the core primitive and evidence repository for the Silence-as-Control / Proof-of-Resonance framing.

`por-copilot-bridge` is an applied coding-agent release-governance bridge. It evaluates coding-agent output as a release candidate and assigns a deterministic bridge state before that candidate advances toward merge.

For v0.1.1, compatibility is by state and schema only. The bridge does not depend on, import, or wrap `silence-as-control`. The compatibility adapter exposes local bridge decisions as a small Proof-of-Resonance-shaped payload with `por_state`, `decision`, `risk_level`, `reasons`, `required_evidence`, and `control_layer` fields.

AI coding-agent output is a candidate, not a release. Generation is not release. Merge must be earned through bounded review, evidence, and release governance.

`NEEDS_REVIEW` is an operational escalation state used by this bridge when a candidate may be valid but lacks enough release evidence or requires human review. It is not a replacement for the core binary primitive in the Silence-as-Control framing.

This bridge makes no claim of universal safety, automatic correctness, model improvement, or autonomous release authority. It is a small deterministic control layer for coding-agent release governance.
