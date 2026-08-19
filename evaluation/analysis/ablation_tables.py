from __future__ import annotations


def make_ablation_markdown(rows: list[dict]) -> str:
    headers = ["Metric", "H0", "H1", "H2", "H3", "Delta H0->H3"]
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        lines.append(
            "| {metric} | {H0} | {H1} | {H2} | {H3} | {delta} |".format(
                metric=r.get("metric", ""),
                H0=r.get("H0", ""),
                H1=r.get("H1", ""),
                H2=r.get("H2", ""),
                H3=r.get("H3", ""),
                delta=r.get("delta", ""),
            )
        )
    return "\n".join(lines)
