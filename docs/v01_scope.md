# v0.1 scope

v0.1 is a compact demonstration of release governance for AI coding-agent outputs.

## Included

- Python package metadata in `pyproject.toml`
- deterministic proposal models
- deterministic evidence helpers
- deterministic risk rules
- a small decision router
- a public `evaluate_proposal` function
- a five-case demo script
- tests for major decision paths
- concise architecture and taxonomy documentation

## Excluded

v0.1 does not include:

- autonomous agent behavior
- GitHub App integration
- SaaS dashboard
- IDE plugin
- LLM judge
- LangChain integration
- SDK surface beyond the small package API
- complex orchestration
- auto-execution
- API keys or external services

## Release-governance claim

The bounded claim is that coding-agent output should be treated as a candidate, not a release. The bridge assigns explicit release state before a candidate can move forward.
