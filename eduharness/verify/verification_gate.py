from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from eduharness.core.types import MasterySnapshot, VerifyDecision
from eduharness.verify.contract_engine import decide_action, load_contract
from eduharness.verify.intent_classifier import classify_intent
from eduharness.verify.mastery_check import estimate_mastery


@dataclass
class VerificationResult:
    intent_label: str
    adversarial_score: float
    mastery: MasterySnapshot
    decision: VerifyDecision


def _load_concept_map(path: str) -> dict:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def run_verification(
    student_input: str,
    contract_path: str,
    concept_map_path: str,
    assessment_mode: str = "practice",
) -> VerificationResult:
    intent, score = classify_intent(student_input)
    mastery = estimate_mastery(student_input, concept_map_path)
    contract = load_contract(contract_path)
    concept_map = _load_concept_map(concept_map_path)
    decision = decide_action(intent, mastery, assessment_mode, contract, concept_map)
    return VerificationResult(intent_label=intent, adversarial_score=score, mastery=mastery, decision=decision)
