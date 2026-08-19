from __future__ import annotations

import json
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def simple_accuracy(tasks: list[dict]) -> float:
    labeled = [t for t in tasks if t.get("annotator_label")]
    if not labeled:
        return 0.0
    ok = sum(1 for t in labeled if t.get("annotator_label") == t.get("gold_label"))
    return ok / len(labeled)


def main() -> None:
    tasks_path = Path("evaluation/data/results/e6_annotation_tasks.jsonl")
    tasks = load_jsonl(tasks_path)
    labeled = [t for t in tasks if t.get("annotator_label")]
    acc = simple_accuracy(tasks)

    out = Path("evaluation/data/results/e6_annotation_summary.md")
    out.write_text(
        "# E6 Annotation Summary\n\n"
        f"- Total tasks: {len(tasks)}\n"
        f"- Labeled tasks: {len(labeled)}\n"
        f"- Accuracy vs gold (single annotator): {acc:.3f}\n",
        encoding="utf-8",
    )
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
