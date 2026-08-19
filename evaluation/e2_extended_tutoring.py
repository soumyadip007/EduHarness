from __future__ import annotations

from evaluation.metrics.educlaw_metrics import delta_solve_rate, plateau_day



def run_e2_stub() -> dict[str, float | int]:
    series = [0.3, 0.36, 0.43, 0.49, 0.53, 0.55, 0.56]
    return {
        "delta_solve_rate": delta_solve_rate(series),
        "plateau_day": plateau_day(series),
        "final_solve_rate": series[-1],
    }
