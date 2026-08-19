from __future__ import annotations


def daily_deltas(series: list[float]) -> list[float]:
    if len(series) < 2:
        return []
    return [series[i] - series[i - 1] for i in range(1, len(series))]


def summary_curve(series: list[float]) -> dict:
    if not series:
        return {"start": 0.0, "end": 0.0, "gain": 0.0}
    return {"start": series[0], "end": series[-1], "gain": series[-1] - series[0]}
