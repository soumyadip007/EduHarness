from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evaluation.analysis.ablation_tables import make_ablation_markdown


if __name__ == "__main__":
    root = Path("evaluation/data/results")
    root.mkdir(parents=True, exist_ok=True)

    # Example export payload; replace with actual experiment outputs.
    rows = [
        {"metric": "Safety", "H0": 0.42, "H1": 0.70, "H2": 0.69, "H3": 0.71, "delta": 0.29},
        {"metric": "Delta Solve", "H0": 0.08, "H1": 0.09, "H2": 0.12, "H3": 0.13, "delta": 0.05},
    ]

    md = make_ablation_markdown(rows)
    (root / "ablation_table.md").write_text(md + "\n", encoding="utf-8")
    (root / "ablation_table.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print("Exported ablation table to evaluation/data/results/")
