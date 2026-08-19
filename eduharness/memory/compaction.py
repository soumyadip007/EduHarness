from __future__ import annotations

from sqlalchemy import select

from eduharness.memory.schema import LearnerState, SessionSummary, TeacherOverride



def compact_history(session_factory, student_id: str, course_id: str, keep_last: int = 20) -> dict:
    with session_factory() as db:
        row = db.execute(
            select(LearnerState).where(LearnerState.student_id == student_id, LearnerState.course_id == course_id)
        ).scalar_one_or_none()
        if row is None:
            return {"compacted": False, "reason": "missing learner_state"}

        history = list(row.scaffold_history or [])
        if len(history) <= keep_last:
            return {"compacted": False, "reason": "below threshold"}

        removed = history[:-keep_last]
        kept = history[-keep_last:]
        row.scaffold_history = kept

        active_overrides = db.execute(
            select(TeacherOverride).where(
                TeacherOverride.student_id == student_id,
                TeacherOverride.course_id == course_id,
                TeacherOverride.active.is_(True),
            )
        ).scalars().all()

        summary = (
            f"Compacted {len(removed)} scaffold events; kept {len(kept)}. "
            f"Protected active overrides: {len(active_overrides)}"
        )
        db.add(SessionSummary(student_id=student_id, course_id=course_id, summary_text=summary, turn_count=len(removed)))
        db.commit()

        return {"compacted": True, "removed": len(removed), "kept": len(kept), "active_overrides": len(active_overrides)}
