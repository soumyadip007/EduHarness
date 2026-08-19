from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BKTParams:
    p_transit: float = 0.2
    p_guess: float = 0.2
    p_slip: float = 0.1


def update_mastery(prior: float, correct: bool, params: BKTParams | None = None) -> float:
    p = params or BKTParams()
    prior = min(max(prior, 0.0), 1.0)

    if correct:
        num = prior * (1 - p.p_slip)
        den = num + (1 - prior) * p.p_guess
    else:
        num = prior * p.p_slip
        den = num + (1 - prior) * (1 - p.p_guess)

    posterior = num / den if den else prior
    learned = posterior + (1 - posterior) * p.p_transit
    return min(max(learned, 0.0), 1.0)
