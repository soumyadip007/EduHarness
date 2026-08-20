from __future__ import annotations

import json
from pathlib import Path

from sqlalchemy import select

from eduharness.memory.memory_read import load_state
from eduharness.pedagogy.progress_plan import _load_concept_map


EXERCISES_DIR = Path("course_content/exercises")


def _load_all_exercises() -> list[dict]:
    exercises: list[dict] = []
    if not EXERCISES_DIR.exists():
        return exercises
    for path in sorted(EXERCISES_DIR.glob("*_exercises.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and item.get("id"):
                    exercises.append(item)
    return exercises


def _prerequisites_met(concept_id: str, mastery: dict[str, float], concept_map: list[dict]) -> bool:
    entry = next((c for c in concept_map if c.get("id") == concept_id), None)
    if not entry:
        return True
    return all(float(mastery.get(p, 0.0)) >= 0.45 for p in entry.get("prerequisites", []))


def select_questions(
    session_factory,
    student_id: str,
    course_id: str = "cs101_python",
    count: int = 3,
    concept_map_path: str = "configs/concept_maps/python_intro.yaml",
) -> list[dict]:
    """Pick exercises targeting focus concepts based on mastery and prerequisites."""
    state = load_state(session_factory, student_id=student_id, course_id=course_id)
    mastery = state.mastery or {}
    concept_map = _load_concept_map(concept_map_path)
    all_exercises = _load_all_exercises()

    ranked_concepts: list[tuple[str, float]] = []
    for concept in concept_map:
        cid = concept.get("id", "")
        if not cid:
            continue
        if not _prerequisites_met(cid, mastery, concept_map):
            continue
        score = float(mastery.get(cid, 0.0))
        if score < 0.75:
            ranked_concepts.append((cid, score))

    ranked_concepts.sort(key=lambda x: x[1])
    focus = [c for c, _ in ranked_concepts[:3]] or [c.get("id") for c in concept_map if c.get("id")][:1]

    selected: list[dict] = []
    for concept in focus:
        pool = [e for e in all_exercises if e.get("concept") == concept]
        pool.sort(key=lambda e: e.get("id", ""))
        for exercise in pool:
            if exercise not in selected:
                selected.append(
                    {
                        **exercise,
                        "target_concept": concept,
                        "student_mastery": round(float(mastery.get(concept, 0.0)), 3),
                        "selection_reason": "low_mastery_focus" if mastery.get(concept, 0) < 0.5 else "reinforcement",
                    }
                )
            if len(selected) >= count:
                break
        if len(selected) >= count:
            break

    if len(selected) < count:
        for exercise in all_exercises:
            if exercise not in selected:
                selected.append({**exercise, "target_concept": exercise.get("concept", ""), "selection_reason": "fallback"})
            if len(selected) >= count:
                break

    return selected[:count]
