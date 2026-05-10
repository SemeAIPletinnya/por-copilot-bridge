# por-copilot-bridge

`por-copilot-bridge` is a small, deterministic release-governance bridge for AI coding-agent outputs.

It demonstrates a narrow thesis:

> AI coding agents need release governance, not just better generation. Implementation is not release. Merge must be earned.

## What this is

This package evaluates a coding-agent proposal as a release candidate. The proposal can include source, title, body, changed files, commands, claims, and evidence. The bridge returns an explicit release state:

- `PROCEED` for low-risk changes such as docs-only edits, comment-only edits, read-only explanations, harmless formatting, and non-executable markdown.
- `NEEDS_REVIEW` for changes that may be valid but require release evidence or human review.
- `SILENCE` for proposals that should not advance because they contain destructive commands, approval bypasses, disabled safeguards, exposed secrets, forced main-branch pushes, or destructive migrations without rollback.

## What this is not

This is not a coding agent. It does not generate code.

This is not an auto-execution system. It does not run commands, mutate repositories, deploy services, or merge pull requests.

This is not a GitHub App, SaaS dashboard, IDE plugin, SDK, LLM judge, LangChain integration, or autonomous agent.

It is release-governance middleware: a deterministic gate that assigns release state to a candidate produced elsewhere.

## Relationship to Silence-as-Control

`silence-as-control` is the core primitive and evidence repository for the Silence-as-Control / Proof-of-Resonance framing. `por-copilot-bridge` is an applied coding-agent release-governance bridge compatible by state and schema in v0.1.1, without a direct package dependency.

AI coding-agent output is a candidate, not a release. Generation is not release, and merge must be earned through bounded review, evidence, and release governance. The bridge's `NEEDS_REVIEW` state is an operational escalation state, not a replacement for the core binary primitive.

See [docs/silence_as_control_integration.md](docs/silence_as_control_integration.md) for the bounded integration notes.

## Design position

Generation is not release.

AI coding-agent output is only a candidate. The candidate may be useful, but usefulness is not enough to merge. The bridge makes the release state explicit and separates implementation output from release permission.

The bridge is intentionally bounded. It uses deterministic rules, not model judgment. It makes conservative decisions based on proposal content, changed paths, commands, claims, and supplied evidence.

## Proposal shape

```python
proposal = {
    "source": "coding-agent",
    "title": "Update service configuration",
    "body": "Changes timeout settings.",
    "files_changed": ["service/config.yaml"],
    "commands": [],
    "claims": ["verified works"],
    "evidence": [],
}
```

## Usage

```python
from por_copilot_bridge import evaluate_proposal

result = evaluate_proposal(proposal)
print(result.as_dict())
```

Example output:

```python
{
    "decision": "NEEDS_REVIEW",
    "risk_level": "medium",
    "reasons": ["env/config mutation", "verification claim without evidence", "missing rollback note for operational change"],
    "required_evidence": ["configuration diff review", "passing test/check evidence", "rollback note"],
}
```

## Demo

Run the deterministic demo:

```bash
PYTHONPATH=src python examples/config_mutation_gate.py
```

It prints five fixed cases:

1. safe docs edit -> `PROCEED`
2. config mutation without evidence -> `NEEDS_REVIEW`
3. fake "verified works" claim without evidence -> `NEEDS_REVIEW`
4. approval bypass / skip CI -> `SILENCE`
5. destructive shell command -> `SILENCE`

### PoR-compatible payload demo

Run the applied payload demo:

```bash
python examples/por_payload_demo.py
```

Compact example output:

```json
{
  "control_layer": "por-copilot-bridge",
  "decision": "NEEDS_REVIEW",
  "por_state": "NEEDS_REVIEW",
  "reasons": ["env/config mutation", "missing rollback note for operational change"],
  "required_evidence": ["configuration diff review", "rollback note"],
  "risk_level": "medium"
}
```

## Development

```bash
python -m pytest
```

The package has no runtime dependency on API keys or external services.
