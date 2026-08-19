from __future__ import annotations


def intervention_rate(escalations: int, tutoring_hours: float) -> float:
    if tutoring_hours <= 0:
        return 0.0
    return escalations / tutoring_hours


def patch_latency_seconds(applied_at_ts: float, created_at_ts: float) -> float:
    return max(0.0, applied_at_ts - created_at_ts)


def patch_success_rate(successes: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return successes / total
