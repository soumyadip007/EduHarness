from __future__ import annotations

from pathlib import Path

import yaml

from eduharness.core.types import MasterySnapshot, VerifyDecision


def load_contract(path: str) -> dict:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def decide_action(intent: str, mastery: MasterySnapshot, assessment_mode: str, contract: dict) -> VerifyDecision:
    if intent == "off_topic":
        return VerifyDecision(action="withhold", reason="off-topic request")

    if intent == "answer_inducing":
        return VerifyDecision(action="hint_L1", reason="answer-inducing behavior")

    if intent == "exam_sensitive" or assessment_mode == "exam":
        return VerifyDecision(action="withhold", reason="exam mode protection")

    mean_mastery = 0.0
    if mastery.concept_mastery:
        mean_mastery = sum(mastery.concept_mastery.values()) / len(mastery.concept_mastery)

    if mean_mastery >= 0.75:
        return VerifyDecision(action="allow_full", reason="sufficient mastery")
    if mean_mastery >= 0.5:
        return VerifyDecision(action="hint_L2", reason="partial mastery")
    return VerifyDecision(action="hint_L1", reason="low mastery")
