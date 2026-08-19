from __future__ import annotations

from evaluation.metrics.longtutor_metrics import history_utilization, macro_f1



def run_e3_stub() -> dict[str, float]:
    return {
        "macro_f1": macro_f1(tp=22, fp=10, fn=12),
        "history_utilization": history_utilization([2.0, 2.5, 3.0, 2.8]),
    }
