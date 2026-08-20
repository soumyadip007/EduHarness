from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import yaml
from sqlalchemy import select

from eduharness.memory.schema import ProgressPlan
from eduharness.memory.memory_read import load_state


def _load_concept_map(concept_map_path: str) -> list[dict]:
    data = yaml.safe_load(Path(concept_map_path).read_text(encoding="utf-8"))
    return data.get("concepts", []) if isinstance(data, dict) else []


def generate_progress_plan(
    session_factory,
    student_id: str,
    course_id: str = "cs101_python",
    concept_map_path: str = "configs/concept_maps/python_intro.yaml",
) -> dict:
    """Build a dependency-aware long-horizon learning plan from mastery state."""
    state = load_state(session_factory, student_id=student_id, course_id=course_id)
    mastery = state.mastery or {}
    concepts = _load_concept_map(concept_map_path)

    steps: list[dict] = []
    for concept in concepts:
        cid = concept.get("id", "")
        if not cid:
            continue
        prereqs = concept.get("prerequisites", [])
        prereq_scores = [float(mastery.get(p, 0.0)) for p in prereqs]
        prereqs_met = all(s >= 0.55 for s in prereq_scores) if prereqs else True
        score = float(mastery.get(cid, 0.0))
        if score >= 0.75:
            status = "mastered"
        elif not prereqs_met:
            status = "blocked"
        elif score >= 0.5:
            status = "reinforce"
        else:
            status = "focus"
        steps.append(
            {
                "concept": cid,
                "mastery": round(score, 3),
                "prerequisites": prereqs,
                "prerequisites_met": prereqs_met,
                "status": status,
                "recommended_action": _recommend_action(status),
            }
        )

    plan = {
        "student_id": student_id,
        "course_id": course_id,
        "generated_at": datetime.now(UTC).isoformat(),
        "focus_concepts": [s["concept"] for s in steps if s["status"] in {"focus", "reinforce"}][:3],
        "steps": steps,
    }

    with session_factory() as db:
        row = db.execute(
            select(ProgressPlan).where(
                ProgressPlan.student_id == student_id,
                ProgressPlan.course_id == course_id,
            )
        ).scalar_one_or_none()
        if row is None:
            row = ProgressPlan(student_id=student_id, course_id=course_id, plan=plan)
            db.add(row)
        else:
            row.plan = plan
            row.updated_at = datetime.now(UTC)
        db.commit()

    return plan


def _recommend_action(status: str) -> str:
    return {
        "mastered": "Move to applied exercises",
        "reinforce": "Short practice set with hints",
        "focus": "Guided scaffolding with worked examples",
        "blocked": "Review prerequisite concepts first",
    }.get(status, "Continue practice")
