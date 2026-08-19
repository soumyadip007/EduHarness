from __future__ import annotations

import csv
from pathlib import Path


def mean(vals: list[float]) -> float:
    return sum(vals) / len(vals) if vals else 0.0


def main() -> None:
    inp = Path("evaluation/data/results/sample_pilot_anon.csv")
    if not inp.exists():
        print("Missing anonymized pilot data file")
        return
    rows = list(csv.DictReader(inp.read_text(encoding="utf-8").splitlines()))
    pre = [float(r["pre_score"]) for r in rows]
    post = [float(r["post_score"]) for r in rows]
    gain = [b - a for a, b in zip(pre, post)]

    out = Path("evaluation/data/results/pilot_analysis_summary.md")
    out.write_text(
        "# Pilot Analysis Summary\n\n"
        f"- Participants: {len(rows)}\n"
        f"- Mean pre-score: {mean(pre):.2f}\n"
        f"- Mean post-score: {mean(post):.2f}\n"
        f"- Mean gain: {mean(gain):.2f}\n",
        encoding="utf-8",
    )
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
