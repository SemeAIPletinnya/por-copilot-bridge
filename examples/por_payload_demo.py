"""Deterministic PoR-compatible payload demo for the bridge."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from por_copilot_bridge import evaluate_proposal, result_to_por_payload


PROPOSAL = {
    "source": "coding-agent",
    "title": "Update service configuration",
    "body": "Change runtime timeout settings.",
    "files_changed": ["service/config.yaml"],
    "commands": [],
    "claims": [],
    "evidence": [],
}


def main() -> None:
    result = evaluate_proposal(PROPOSAL)
    payload = result_to_por_payload(result)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
