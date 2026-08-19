from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select

from eduharness.memory.schema import LearnerState, TeacherOverride


@dataclass
class ReadResult:
    mastery: dict
    misconceptions: list
    scaffold_history: list
    teacher_overrides: list[dict]



def load_state(session_factory, student_id: str, course_id: str) -> ReadResult:
    with session_factory() as db:
        row = db.execute(
            select(LearnerState).where(LearnerState.student_id == student_id, LearnerState.course_id == course_id)
        ).scalar_one_or_none()
        overrides = db.execute(
            select(TeacherOverride).where(
                TeacherOverride.student_id == student_id,
                TeacherOverride.course_id == course_id,
                TeacherOverride.active.is_(True),
            )
        ).scalars().all()

    if row is None:
        return ReadResult(mastery={}, misconceptions=[], scaffold_history=[], teacher_overrides=[])

    return ReadResult(
        mastery=row.mastery or {},
        misconceptions=row.misconceptions or [],
        scaffold_history=row.scaffold_history or [],
        teacher_overrides=[
            {"teacher_id": o.teacher_id, "rule_key": o.rule_key, "rule_value": o.rule_value} for o in overrides
        ],
    )


def format_state_for_context(state: ReadResult) -> str:
    return (
        f"Mastery: {state.mastery}\n"
        f"Misconceptions: {state.misconceptions}\n"
        f"Scaffold history length: {len(state.scaffold_history)}\n"
        f"Active overrides: {state.teacher_overrides}"
    )
