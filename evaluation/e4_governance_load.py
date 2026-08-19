from __future__ import annotations

from evaluation.metrics.governance_metrics import intervention_rate, patch_success_rate


def run_e4_stub() -> dict[str, float]:
    escalations = 14
    hours = 8.0
    successes = 10
    total_patches = 12
    return {
        "intervention_rate": intervention_rate(escalations, hours),
        "patch_success_rate": patch_success_rate(successes, total_patches),
    }
