from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    sim_path = Path("evaluation/data/results/phase6_learning_curve.json")
    pilot_path = Path("evaluation/data/results/pilot_analysis_summary.md")

    if not sim_path.exists() or not pilot_path.exists():
        print("Missing inputs for comparison")
        return

    sim = json.loads(sim_path.read_text(encoding="utf-8"))
    sim_gain = float(sim["summary"]["gain"])

    text = pilot_path.read_text(encoding="utf-8")
    marker = "- Mean gain: "
    idx = text.find(marker)
    real_gain = 0.0
    if idx >= 0:
        line = text[idx + len(marker):].splitlines()[0].strip()
        real_gain = float(line)

    out = Path("evaluation/data/results/simulated_vs_real_comparison.md")
    out.write_text(
        "# Simulated vs Real Gain Comparison\n\n"
        f"- Simulated gain (E2 proxy): {sim_gain:.3f}\n"
        f"- Real pilot mean gain: {real_gain:.3f}\n"
        f"- Absolute gap: {abs(sim_gain - real_gain):.3f}\n",
        encoding="utf-8",
    )
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
