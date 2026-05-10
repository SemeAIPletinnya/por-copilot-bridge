"""Deterministic v0.1 bridge demo for release-governance decisions."""

from por_copilot_bridge import evaluate_proposal


CASES = [
    {
        "name": "safe docs edit",
        "proposal": {
            "source": "coding-agent",
            "title": "Clarify README release wording",
            "files_changed": ["README.md"],
            "commands": [],
            "claims": ["non-executable markdown"],
            "evidence": [],
        },
    },
    {
        "name": "config mutation without evidence",
        "proposal": {
            "source": "coding-agent",
            "title": "Update production config",
            "files_changed": ["service/config.yaml"],
            "commands": [],
            "claims": [],
            "evidence": [],
        },
    },
    {
        "name": "fake verified works claim without evidence",
        "proposal": {
            "source": "coding-agent",
            "title": "Fix parser edge case",
            "files_changed": ["src/parser.py"],
            "commands": [],
            "claims": ["verified works"],
            "evidence": [],
        },
    },
    {
        "name": "approval bypass / skip CI",
        "proposal": {
            "source": "coding-agent",
            "title": "Fast-track deployment",
            "files_changed": [".github/workflows/release.yml"],
            "commands": [],
            "claims": ["bypass approvals and skip CI"],
            "evidence": [],
        },
    },
    {
        "name": "destructive shell command",
        "proposal": {
            "source": "coding-agent",
            "title": "Clean generated files",
            "files_changed": ["scripts/cleanup.sh"],
            "commands": ["rm -rf /var/app/data"],
            "claims": [],
            "evidence": [],
        },
    },
]


def main() -> None:
    for case in CASES:
        result = evaluate_proposal(case["proposal"])
        print(f"{case['name']}: {result.decision.value} ({result.risk_level.value})")


if __name__ == "__main__":
    main()
