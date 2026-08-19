from __future__ import annotations


def state_divergence(inferred: dict[str, float], observed: dict[str, float]) -> float:
    concepts = set(inferred) | set(observed)
    if not concepts:
        return 0.0
    return sum(abs(float(inferred.get(c, 0.0)) - float(observed.get(c, 0.0))) for c in concepts) / len(concepts)


def contradiction_rate(total_turns: int, contradictions: int) -> float:
    if total_turns <= 0:
        return 0.0
    return contradictions / total_turns
