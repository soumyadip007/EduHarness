from __future__ import annotations

from evaluation.metrics.tti import compute_tti


WEIGHT_PRESETS = {
    "equal": {
        "safety_adversarial": 1,
        "helpfulness": 1,
        "delta_solve_rate": 1,
        "state_divergence_inv": 1,
        "history_utilization": 1,
        "teacher_burden_inv": 1,
        "policy_compliance": 1,
    },
    "safety_heavy": {
        "safety_adversarial": 2,
        "helpfulness": 1,
        "delta_solve_rate": 1,
        "state_divergence_inv": 1,
        "history_utilization": 1,
        "teacher_burden_inv": 0.5,
        "policy_compliance": 1,
    },
    "learning_heavy": {
        "safety_adversarial": 1,
        "helpfulness": 1,
        "delta_solve_rate": 2,
        "state_divergence_inv": 1,
        "history_utilization": 2,
        "teacher_burden_inv": 0.5,
        "policy_compliance": 1,
    },
    "governance_heavy": {
        "safety_adversarial": 1,
        "helpfulness": 1,
        "delta_solve_rate": 1,
        "state_divergence_inv": 1,
        "history_utilization": 1,
        "teacher_burden_inv": 2,
        "policy_compliance": 2,
    },
    "supervisor_tuned": {
        "safety_adversarial": 1.5,
        "helpfulness": 1,
        "delta_solve_rate": 1.5,
        "state_divergence_inv": 1,
        "history_utilization": 1.5,
        "teacher_burden_inv": 1,
        "policy_compliance": 1.5,
    },
}


def run_tti_sensitivity(metrics: dict[str, float]) -> dict[str, float]:
    return {name: compute_tti(metrics, w) for name, w in WEIGHT_PRESETS.items()}
