# Architecture

`por-copilot-bridge` is a small release-governance boundary between coding-agent output and release action.

## Boundary

The bridge accepts a proposal object and returns a deterministic decision. It does not call an LLM, execute shell commands, open pull requests, deploy software, or merge code.

## Components

- `models.py` defines proposal, evidence, decision, and risk data structures.
- `evidence.py` detects verification claims and explicit evidence supplied with the proposal.
- `risk_rules.py` applies deterministic path, command, claim, and evidence rules.
- `router.py` maps findings to `PROCEED`, `NEEDS_REVIEW`, or `SILENCE`.
- `bridge.py` exposes the public `evaluate_proposal` API.

## Decision flow

1. Normalize the proposal input.
2. Evaluate deterministic risk findings.
3. Route critical blocked findings to `SILENCE`.
4. Route review findings to `NEEDS_REVIEW`.
5. Allow clearly low-risk docs, comments, read-only explanations, or formatting changes to `PROCEED`.
6. Send unclassified executable or behavioral changes to `NEEDS_REVIEW`.

## Non-goals

The bridge is not an autonomous agent, GitHub App, SaaS dashboard, IDE plugin, LLM judge, LangChain integration, SDK, complex orchestrator, or auto-execution system.
