# Risk taxonomy

The v0.1 taxonomy is intentionally small and deterministic.

## PROCEED

`PROCEED` is limited to low-risk candidates:

- docs-only edits
- comment-only edits
- read-only explanations
- harmless formatting
- non-executable markdown

## NEEDS_REVIEW

`NEEDS_REVIEW` means the proposal may be valid, but release must be earned with evidence or human review:

- environment or configuration mutation
- dependency changes
- CI/CD changes
- database migrations
- API behavior changes
- permission or scope changes
- "tests passed" or "verified works" claims without evidence
- test mismatch
- missing rollback note for operational change
- unclassified executable or behavioral changes

## SILENCE

`SILENCE` means the proposal should not advance through the release bridge:

- destructive shell commands
- `rm -rf` or mass delete behavior
- approval bypasses
- disabling authentication
- skipping CI
- exposing secrets
- force-pushing `main`
- granting admin access
- destructive migration without rollback

## Risk levels

- `low`: narrow safe path
- `medium`: review required for bounded release risk
- `high`: operational, CI, migration, or permission-sensitive risk
- `critical`: blocked behavior that maps to `SILENCE`
