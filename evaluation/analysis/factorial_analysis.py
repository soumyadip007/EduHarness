from __future__ import annotations


def summarize_model_harness_grid(cells: list[dict]) -> dict:
    # cells: [{model:'A', harness:'H0', tti:0.5}, ...]
    model_means: dict[str, list[float]] = {}
    harness_means: dict[str, list[float]] = {}
    for c in cells:
        model_means.setdefault(c["model"], []).append(float(c["tti"]))
        harness_means.setdefault(c["harness"], []).append(float(c["tti"]))

    return {
        "model_means": {k: sum(v) / len(v) for k, v in model_means.items() if v},
        "harness_means": {k: sum(v) / len(v) for k, v in harness_means.items() if v},
        "cell_count": len(cells),
    }
