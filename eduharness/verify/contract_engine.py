from __future__ import annotations

from pathlib import Path

import yaml

from eduharness.core.types import MasterySnapshot, VerifyDecision


def load_contract(path: str) -> dict:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _target_concept(mastery: MasterySnapshot) -> str | None:
    if not mastery.concept_mastery:
        return None
    return max(mastery.concept_mastery, key=mastery.concept_mastery.get)


def _prerequisites_met(concept_id: str, concept_map: dict, mastery: MasterySnapshot) -> bool:
    concepts = concept_map.get("concepts", [])
    entry = next((c for c in concepts if c.get("id") == concept_id), None)
    if not entry:
        return True
    prereqs = entry.get("prerequisites", [])
    return all(mastery.concept_mastery.get(p, 0.0) >= 0.45 for p in prereqs)


def decide_action(
    intent: str,
    mastery: MasterySnapshot,
    assessment_mode: str,
    contract: dict,
    concept_map: dict | None = None,
) -> VerifyDecision:
    if intent == "off_topic":
        return VerifyDecision(action="withhold", reason="off-topic request")

    if intent == "answer_inducing":
        return VerifyDecision(action="hint_L1", reason="answer-inducing behavior")

    if intent == "exam_sensitive" or assessment_mode == "exam":
        return VerifyDecision(action="withhold", reason="exam mode protection")

    concept_map = concept_map or {}
    target = _target_concept(mastery)
    if target and concept_map:
        concepts = concept_map.get("concepts", [])
        entry = next((c for c in concepts if c.get("id") == target), None)
        if entry and not _prerequisites_met(target, concept_map, mastery):
            blocked = [
                p for p in entry.get("prerequisites", []) if mastery.concept_mastery.get(p, 0.0) < 0.45
            ]
            return VerifyDecision(
                action="hint_L1",
                reason=f"prerequisite_gap:{','.join(blocked) or target}",
            )

    if target:
        score = mastery.concept_mastery.get(target, 0.0)
        if score >= 0.75:
            return VerifyDecision(action="allow_full", reason=f"sufficient mastery on {target}")
        if score >= 0.5:
            return VerifyDecision(action="hint_L2", reason=f"partial mastery on {target}")
        return VerifyDecision(action="hint_L1", reason=f"low mastery on {target}")

    mean_mastery = 0.0
    if mastery.concept_mastery:
        mean_mastery = sum(mastery.concept_mastery.values()) / len(mastery.concept_mastery)

    if mean_mastery >= 0.75:
        return VerifyDecision(action="allow_full", reason="sufficient mastery")
    if mean_mastery >= 0.5:
        return VerifyDecision(action="hint_L2", reason="partial mastery")
    return VerifyDecision(action="hint_L1", reason="low mastery")
