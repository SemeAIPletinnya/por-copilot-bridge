import json
import subprocess
import sys
from pathlib import Path


def test_por_payload_demo_prints_expected_payload():
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "examples/por_payload_demo.py"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)

    assert payload["por_state"] == "NEEDS_REVIEW"
    assert payload["decision"] == "NEEDS_REVIEW"
    assert payload["risk_level"] == "medium"
    assert payload["control_layer"] == "por-copilot-bridge"
    assert "env/config mutation" in payload["reasons"]
    assert "configuration diff review" in payload["required_evidence"]
