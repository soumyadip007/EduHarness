from __future__ import annotations

import json
from pathlib import Path

from evaluation.metrics.shape_metrics import helpfulness_score, pedagogy_score, safety_score


def run_e1_stub(prompts_file: str) -> dict[str, float]:
    prompts = json.loads(Path(prompts_file).read_text(encoding="utf-8"))
    total = len(prompts)
    # Placeholder deterministic demo until full judge pipeline is added.
    return {
        "safety": safety_score(total, int(total * 0.7)),
        "helpfulness": helpfulness_score(total, int(total * 0.6)),
        "pedagogy": pedagogy_score(total, int(total * 0.65)),
    }


if __name__ == "__main__":
    results = run_e1_stub("evaluation/data/adversarial_prompts/v0.1.jsonl")
    print(json.dumps(results, indent=2))
