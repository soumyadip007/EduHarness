from __future__ import annotations


def detect_drift(inferred_mastery: dict[str, float], observed_mastery: dict[str, float], threshold: float = 0.3) -> dict:
    drifted: dict[str, float] = {}
    all_concepts = set(inferred_mastery) | set(observed_mastery)
    for concept in all_concepts:
        inf = float(inferred_mastery.get(concept, 0.0))
        obs = float(observed_mastery.get(concept, 0.0))
        diff = abs(inf - obs)
        if diff > threshold:
            drifted[concept] = round(diff, 4)
    return {"drift_detected": bool(drifted), "concept_deltas": drifted}
