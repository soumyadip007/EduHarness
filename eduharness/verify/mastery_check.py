from __future__ import annotations

from pathlib import Path

import yaml

from eduharness.core.types import MasterySnapshot


def _load_concepts(concept_map_path: str) -> list[dict]:
    data = yaml.safe_load(Path(concept_map_path).read_text(encoding="utf-8"))
    return data.get("concepts", []) if isinstance(data, dict) else []


def estimate_mastery(student_input: str, concept_map_path: str) -> MasterySnapshot:
    concepts = _load_concepts(concept_map_path)
    text = student_input.lower()
    mastery: dict[str, float] = {}

    for c in concepts:
        cid = c.get("id", "")
        if not cid:
            continue
        mastery[cid] = 0.6 if cid in text else 0.3

    prerequisites_met = any(v >= 0.5 for v in mastery.values()) if mastery else False
    return MasterySnapshot(concept_mastery=mastery, prerequisites_met=prerequisites_met)
