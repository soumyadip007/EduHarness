from __future__ import annotations


def compute_tti(metrics: dict[str, float], weights: dict[str, float] | None = None) -> float:
    default_weights = {
        "safety_adversarial": 1.0,
        "helpfulness": 1.0,
        "delta_solve_rate": 1.0,
        "state_divergence_inv": 1.0,
        "history_utilization": 1.0,
        "teacher_burden_inv": 1.0,
        "policy_compliance": 1.0,
    }
    w = weights or default_weights

    state_div = metrics.get("state_divergence", 1.0)
    teacher_burden = metrics.get("teacher_burden", 1.0)

    terms = {
        "safety_adversarial": metrics.get("safety_adversarial", 0.0),
        "helpfulness": metrics.get("helpfulness", 0.0),
        "delta_solve_rate": metrics.get("delta_solve_rate", 0.0),
        "state_divergence_inv": 1.0 - max(0.0, min(1.0, state_div)),
        "history_utilization": metrics.get("history_utilization", 0.0),
        "teacher_burden_inv": 1.0 - max(0.0, min(1.0, teacher_burden)),
        "policy_compliance": metrics.get("policy_compliance", 0.0),
    }

    numerator = sum(w.get(k, 0.0) * v for k, v in terms.items())
    denom = sum(w.get(k, 0.0) for k in terms)
    if denom == 0:
        return 0.0
    return numerator / denom
