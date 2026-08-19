from __future__ import annotations


def cost_per_1000_turns(total_usd: float, turns: int) -> float:
    if turns <= 0:
        return 0.0
    return (total_usd / turns) * 1000.0


def summarize_costs(cost_rows: list[dict]) -> dict:
    # row = {condition:'H2-mid', usd:12.3, turns:1000}
    out = {}
    for row in cost_rows:
        out[row["condition"]] = {
            "usd": float(row.get("usd", 0.0)),
            "turns": int(row.get("turns", 0)),
            "usd_per_1000": cost_per_1000_turns(float(row.get("usd", 0.0)), int(row.get("turns", 0))),
        }
    return out
