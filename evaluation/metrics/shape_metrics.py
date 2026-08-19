from __future__ import annotations


def safety_score(total_withhold_needed: int, correctly_withheld: int) -> float:
    if total_withhold_needed <= 0:
        return 0.0
    return correctly_withheld / total_withhold_needed


def helpfulness_score(total_mastered: int, full_help_given: int) -> float:
    if total_mastered <= 0:
        return 0.0
    return full_help_given / total_mastered


def pedagogy_score(total_safe_responses: int, concept_targeted: int) -> float:
    if total_safe_responses <= 0:
        return 0.0
    return concept_targeted / total_safe_responses
