from __future__ import annotations


def delta_solve_rate(daily_solve_rates: list[float]) -> float:
    if len(daily_solve_rates) < 2:
        return 0.0
    deltas = [daily_solve_rates[i] - daily_solve_rates[i - 1] for i in range(1, len(daily_solve_rates))]
    return sum(deltas) / len(deltas)


def plateau_day(daily_solve_rates: list[float], threshold: float = 0.01) -> int:
    for i in range(1, len(daily_solve_rates)):
        if abs(daily_solve_rates[i] - daily_solve_rates[i - 1]) < threshold:
            return i + 1
    return len(daily_solve_rates)
