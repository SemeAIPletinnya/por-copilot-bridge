from por_copilot_bridge import Decision, RiskLevel, evaluate_proposal
from por_copilot_bridge.risk_rules import is_docs_only


def test_docs_only_is_safe_path():
    assert is_docs_only(("README.md", "docs/architecture.md"))


def test_config_mutation_needs_review_with_rollback_requirement():
    result = evaluate_proposal(
        {
            "source": "agent",
            "title": "Change runtime config",
            "files_changed": ["service/config.yaml"],
            "commands": [],
            "claims": [],
            "evidence": [],
        }
    )

    assert result.decision is Decision.NEEDS_REVIEW
    assert result.risk_level is RiskLevel.MEDIUM
    assert "env/config mutation" in result.reasons
    assert "rollback note" in result.required_evidence


def test_ci_changes_are_high_risk_review():
    result = evaluate_proposal(
        {
            "source": "agent",
            "title": "Change CI",
            "files_changed": [".github/workflows/test.yml"],
            "commands": [],
            "claims": [],
            "evidence": [{"kind": "note", "detail": "rollback by reverting workflow"}],
        }
    )

    assert result.decision is Decision.NEEDS_REVIEW
    assert result.risk_level is RiskLevel.HIGH
    assert "CI/CD changes" in result.reasons


def test_destructive_command_is_silenced():
    result = evaluate_proposal(
        {
            "source": "agent",
            "title": "Cleanup",
            "files_changed": ["scripts/cleanup.sh"],
            "commands": ["rm -rf build/"],
            "claims": [],
            "evidence": [],
        }
    )

    assert result.decision is Decision.SILENCE
    assert result.risk_level is RiskLevel.CRITICAL
    assert "destructive shell command" in result.reasons


def test_dependency_api_and_permission_changes_need_review():
    cases = [
        ("pyproject.toml", "dependency changes"),
        ("src/public_api.py", "API behavior changes"),
        ("src/auth_policy.py", "permission/scope changes"),
    ]

    for path, reason in cases:
        result = evaluate_proposal(
            {
                "source": "agent",
                "title": "Change guarded surface",
                "files_changed": [path],
                "commands": [],
                "claims": [],
                "evidence": [],
            }
        )

        assert result.decision is Decision.NEEDS_REVIEW
        assert reason in result.reasons


def test_database_migration_with_rollback_still_needs_review():
    result = evaluate_proposal(
        {
            "source": "agent",
            "title": "Add migration",
            "files_changed": ["migrations/0001_add_table.sql"],
            "commands": [],
            "claims": [],
            "evidence": [{"kind": "note", "detail": "rollback by reverting migration"}],
        }
    )

    assert result.decision is Decision.NEEDS_REVIEW
    assert result.risk_level is RiskLevel.HIGH
    assert "database migrations" in result.reasons
