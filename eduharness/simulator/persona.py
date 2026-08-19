from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class Persona:
    persona_id: str
    description: str
    initial_mastery: dict[str, float]


def load_persona(path: str | Path) -> Persona:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return Persona(
        persona_id=data["id"],
        description=data.get("description", ""),
        initial_mastery=data.get("initial_mastery", {}),
    )


def generate_student_response(persona: Persona, concept: str) -> str:
    mastery = persona.initial_mastery.get(concept, 0.0)
    if mastery >= 0.7:
        return f"I think I can solve {concept} with little help."
    if mastery >= 0.4:
        return f"I partially understand {concept}, can you give a hint?"
    return f"I am confused about {concept}. Please scaffold slowly."
