from __future__ import annotations

import json
import random
from datetime import UTC, datetime
from pathlib import Path

LAYER_CHOICES = ["agent", "verify", "memory", "govern"]
INTENT_CHOICES = ["help_seeking", "answer_inducing", "off_topic", "exam_sensitive"]
VERIFY_CHOICES = ["hint_L1", "hint_L2", "withhold", "allow_full", "none"]


def synthesize_trace(i: int, rng: random.Random) -> dict:
    layer = rng.choice(LAYER_CHOICES)
    intent = rng.choice(INTENT_CHOICES)
    verify = rng.choice(VERIFY_CHOICES)
    return {
        "trace_id": f"e6-{i:04d}",
        "session_id": f"sess-{1 + (i // 10):03d}",
        "turn_number": 1 + (i % 10),
        "timestamp": datetime.now(UTC).isoformat(),
        "student_input": f"Student utterance {i}: please help with loops and functions.",
        "intent_label": intent,
        "adversarial_score": round(rng.random(), 3),
        "mastery_snapshot": {"loops": round(rng.uniform(0.2, 0.9), 2), "functions": round(rng.uniform(0.2, 0.9), 2)},
        "verify_decision": verify,
        "contract_rule_fired": "exam mode protection" if intent == "exam_sensitive" else "",
        "agent_output": "Guided hint provided.",
        "post_check_result": rng.choice(["pass", "rewrite", "block"]),
        "memory_update": {"concept": "loops", "prior": 0.4, "post": 0.5},
        "escalation_triggered": layer == "govern",
        "layer_label": layer,
        "latency_ms": {"verify": rng.randint(10, 90), "agent": rng.randint(200, 800)},
        "tokens_used": {"agent": rng.randint(100, 600), "verify": rng.randint(20, 120)},
    }


def build_annotation_pack(n: int = 200, seed: int = 7) -> tuple[Path, Path]:
    rng = random.Random(seed)
    out_dir = Path("evaluation/data/results")
    out_dir.mkdir(parents=True, exist_ok=True)

    traces_path = out_dir / "e6_trace_pool.jsonl"
    tasks_path = out_dir / "e6_annotation_tasks.jsonl"

    traces = [synthesize_trace(i + 1, rng) for i in range(n)]
    tasks = [
        {
            "task_id": f"task-{i+1:04d}",
            "trace_id": t["trace_id"],
            "prompt": "Label primary failure/control layer: agent | verify | memory | govern",
            "trace": t,
            "gold_label": t["layer_label"],
            "annotator_label": None,
            "annotator_id": None,
        }
        for i, t in enumerate(traces)
    ]

    traces_path.write_text("\n".join(json.dumps(x, ensure_ascii=True) for x in traces) + "\n", encoding="utf-8")
    tasks_path.write_text("\n".join(json.dumps(x, ensure_ascii=True) for x in tasks) + "\n", encoding="utf-8")
    return traces_path, tasks_path


if __name__ == "__main__":
    traces_file, tasks_file = build_annotation_pack(n=200)
    print(f"Generated: {traces_file}")
    print(f"Generated: {tasks_file}")
