"""Deterministic risk rules for release-governance decisions."""

from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatch
import shlex

from .evidence import has_passing_test_evidence, has_rollback_evidence, has_verification_claim
from .models import Proposal, RiskLevel


@dataclass(frozen=True)
class RuleFinding:
    risk_level: RiskLevel
    reason: str
    required_evidence: str | None = None
    silence: bool = False


_DESTRUCTIVE_COMMANDS = (
    "rm -rf",
    "rm -fr",
    "git push --force origin main",
    "git push -f origin main",
    "drop database",
    "truncate table",
)

_SILENCE_PHRASES = (
    "bypass approval",
    "bypass approvals",
    "skip ci",
    "disable auth",
    "disabled auth",
    "expose secret",
    "expose secrets",
    "grant admin",
    "grant administrator",
    "force push main",
)

_CONFIG_PATTERNS = ("*.env", ".env*", "*config*", "*.yml", "*.yaml", "*.toml", "*.ini")
_DEPENDENCY_FILES = ("pyproject.toml", "requirements*.txt", "package.json", "package-lock.json", "poetry.lock", "uv.lock")
_CI_PATTERNS = (".github/workflows/*", ".gitlab-ci.yml", "Jenkinsfile", "azure-pipelines.yml")
_MIGRATION_PATTERNS = ("*migration*", "migrations/*", "alembic/versions/*")
_API_PATTERNS = ("*api*", "*routes*", "*schema*", "openapi.*")
_PERMISSION_PATTERNS = ("*auth*", "*permission*", "*policy*", "*scope*", "*role*")
_MARKDOWN_PATTERNS = ("*.md", "docs/*", "README.md")


def _matches_any(path: str, patterns: tuple[str, ...]) -> bool:
    return any(fnmatch(path, pattern) or fnmatch(path.split("/")[-1], pattern) for pattern in patterns)


def _is_main_ref(token: str) -> bool:
    return token in {"main", "refs/heads/main"} or token.endswith(":main") or token.endswith(":refs/heads/main")


def _is_force_push_to_main(command: str) -> bool:
    try:
        tokens = shlex.split(command)
    except ValueError:
        tokens = command.split()

    if len(tokens) < 4 or tokens[:2] != ["git", "push"]:
        return False

    push_args = tokens[2:]
    has_force = any(arg in {"--force", "-f", "--force-with-lease"} or arg.startswith("--force-with-lease=") for arg in push_args)
    targets_main = any(_is_main_ref(arg) for arg in push_args)
    return has_force and targets_main


def is_docs_only(files_changed: tuple[str, ...]) -> bool:
    return bool(files_changed) and all(_matches_any(path, _MARKDOWN_PATTERNS) for path in files_changed)


def is_comment_or_formatting_only(proposal: Proposal) -> bool:
    text = f"{proposal.title}\n{proposal.body}\n{' '.join(proposal.claims)}".lower()
    safe_terms = ("comment-only", "comments only", "formatting only", "harmless formatting", "read-only explanation")
    return any(term in text for term in safe_terms)


def _proposal_text(proposal: Proposal) -> str:
    return "\n".join([proposal.title, proposal.body, *proposal.claims, *proposal.commands]).lower()


def evaluate_risk(proposal: Proposal) -> tuple[RuleFinding, ...]:
    """Return deterministic findings for a proposal."""

    findings: list[RuleFinding] = []
    text = _proposal_text(proposal)

    for command in proposal.commands:
        lowered = command.lower()
        if any(pattern in lowered for pattern in _DESTRUCTIVE_COMMANDS) or _is_force_push_to_main(lowered):
            findings.append(RuleFinding(RiskLevel.CRITICAL, "destructive shell command", silence=True))

    for phrase in _SILENCE_PHRASES:
        if phrase in text:
            findings.append(RuleFinding(RiskLevel.CRITICAL, phrase, silence=True))

    if "destructive migration" in text and not has_rollback_evidence(proposal.evidence, proposal):
        findings.append(
            RuleFinding(
                RiskLevel.CRITICAL,
                "destructive migration without rollback",
                "rollback plan",
                silence=True,
            )
        )

    for path in proposal.files_changed:
        if _matches_any(path, _MARKDOWN_PATTERNS):
            continue
        if _matches_any(path, _CONFIG_PATTERNS):
            findings.append(RuleFinding(RiskLevel.MEDIUM, "env/config mutation", "configuration diff review"))
        if _matches_any(path, _DEPENDENCY_FILES):
            findings.append(RuleFinding(RiskLevel.MEDIUM, "dependency changes", "dependency impact review"))
        if _matches_any(path, _CI_PATTERNS):
            findings.append(RuleFinding(RiskLevel.HIGH, "CI/CD changes", "CI change review"))
        if _matches_any(path, _MIGRATION_PATTERNS):
            findings.append(RuleFinding(RiskLevel.HIGH, "database migrations", "migration plan and rollback note"))
        if _matches_any(path, _API_PATTERNS):
            findings.append(RuleFinding(RiskLevel.MEDIUM, "API behavior changes", "API compatibility evidence"))
        if _matches_any(path, _PERMISSION_PATTERNS):
            findings.append(RuleFinding(RiskLevel.HIGH, "permission/scope changes", "permission review"))

    if has_verification_claim(proposal) and not has_passing_test_evidence(proposal.evidence):
        findings.append(RuleFinding(RiskLevel.MEDIUM, "verification claim without evidence", "passing test/check evidence"))

    if "tests passed" in text and "test" not in " ".join(proposal.commands).lower():
        findings.append(RuleFinding(RiskLevel.MEDIUM, "test mismatch", "test command output"))

    operational = any(f.reason in {"env/config mutation", "CI/CD changes", "database migrations"} for f in findings)
    if operational and not has_rollback_evidence(proposal.evidence, proposal):
        findings.append(RuleFinding(RiskLevel.MEDIUM, "missing rollback note for operational change", "rollback note"))

    return tuple(findings)
