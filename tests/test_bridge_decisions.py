from por_copilot_bridge import Decision, RiskLevel, evaluate_proposal


def test_safe_docs_edit_proceeds():
    result = evaluate_proposal(
        {
            "source": "agent",
            "title": "Update docs",
            "files_changed": ["docs/v01_scope.md"],
            "commands": [],
            "claims": ["non-executable markdown"],
            "evidence": [],
        }
    )

    assert result.decision is Decision.PROCEED
    assert result.risk_level is RiskLevel.LOW


def test_verified_claim_without_evidence_needs_review():
    result = evaluate_proposal(
        {
            "source": "agent",
            "title": "Fix bug",
            "files_changed": ["src/app.py"],
            "commands": [],
            "claims": ["tests passed"],
            "evidence": [],
        }
    )

    assert result.decision is Decision.NEEDS_REVIEW
    assert "verification claim without evidence" in result.reasons
    assert "test mismatch" in result.reasons


def test_verified_claim_with_evidence_but_behavioral_change_still_reviewed():
    result = evaluate_proposal(
        {
            "source": "agent",
            "title": "Fix bug",
            "files_changed": ["src/app.py"],
            "commands": ["pytest"],
            "claims": ["tests passed"],
            "evidence": [{"kind": "test", "detail": "pytest passed", "passed": True}],
        }
    )

    assert result.decision is Decision.NEEDS_REVIEW
    assert result.risk_level is RiskLevel.MEDIUM
    assert result.reasons == ("unclassified executable or behavioral change",)


def test_approval_bypass_skip_ci_silenced():
    result = evaluate_proposal(
        {
            "source": "agent",
            "title": "Deploy quickly",
            "files_changed": [".github/workflows/deploy.yml"],
            "commands": [],
            "claims": ["bypass approvals and skip CI"],
            "evidence": [],
        }
    )

    assert result.decision is Decision.SILENCE
    assert result.risk_level is RiskLevel.CRITICAL
    assert "bypass approvals" in result.reasons
    assert "skip ci" in result.reasons


def test_destructive_migration_without_rollback_silenced():
    result = evaluate_proposal(
        {
            "source": "agent",
            "title": "Apply destructive migration",
            "files_changed": ["migrations/0002_drop_users.sql"],
            "commands": [],
            "claims": ["destructive migration"],
            "evidence": [],
        }
    )

    assert result.decision is Decision.SILENCE
    assert "destructive migration without rollback" in result.reasons
