from __future__ import annotations

from pathlib import Path

import yaml

from eduharness.core.types import MasterySnapshot


CONCEPT_SIGNALS: dict[str, list[str]] = {
    "variables": ["variable", "assign", "=", "int(", "str(", "float("],
    "conditionals": ["if ", "else", "elif", "boolean", "true", "false"],
    "loops": ["for ", "while ", "range(", "iterate", "loop"],
    "functions": ["def ", "return ", "parameter", "argument", "call"],
    "lists": ["list", "[", "]", "append", "index", "slice"],
}


def _load_concepts(concept_map_path: str) -> list[dict]:
    data = yaml.safe_load(Path(concept_map_path).read_text(encoding="utf-8"))
    return data.get("concepts", []) if isinstance(data, dict) else []


def _score_concept(text: str, concept_id: str) -> float:
    signals = CONCEPT_SIGNALS.get(concept_id, [concept_id])
    hits = sum(1 for s in signals if s in text)
    if hits == 0:
        return 0.25
    if hits == 1:
        return 0.45
    if hits == 2:
        return 0.62
    return min(0.85, 0.62 + 0.08 * (hits - 2))


def estimate_mastery(student_input: str, concept_map_path: str) -> MasterySnapshot:
    concepts = _load_concepts(concept_map_path)
    text = student_input.lower()
    mastery: dict[str, float] = {}

    for c in concepts:
        cid = c.get("id", "")
        if not cid:
            continue
        mastery[cid] = round(_score_concept(text, cid), 3)

    prereq_map = {c.get("id"): c.get("prerequisites", []) for c in concepts if c.get("id")}
    prerequisites_met = True
    for cid, prereqs in prereq_map.items():
        if not prereqs:
            continue
        if mastery.get(cid, 0.0) >= 0.5:
            prerequisites_met = prerequisites_met and all(mastery.get(p, 0.0) >= 0.45 for p in prereqs)

    return MasterySnapshot(concept_mastery=mastery, prerequisites_met=prerequisites_met)
