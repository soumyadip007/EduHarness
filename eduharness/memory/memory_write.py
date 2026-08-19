from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select

from eduharness.memory.schema import LearnerState, ProvenanceLog
from eduharness.simulator.bkt_model import update_mastery



def _infer_evidence(student_input: str, agent_output: str) -> bool:
    text = f"{student_input} {agent_output}".lower()
    return any(k in text for k in ("understand", "got it", "thanks", "correct"))


def persist_turn(
    session_factory,
    student_id: str,
    course_id: str,
    concept: str,
    student_input: str,
    agent_output: str,
    scaffold_level: str,
) -> dict:
    with session_factory() as db:
        row = db.execute(
            select(LearnerState).where(LearnerState.student_id == student_id, LearnerState.course_id == course_id)
        ).scalar_one_or_none()

        if row is None:
            row = LearnerState(
                student_id=student_id,
                course_id=course_id,
                mastery={},
                misconceptions=[],
                scaffold_history=[],
                session_count=0,
            )
            db.add(row)
            db.flush()

        prior = float((row.mastery or {}).get(concept, 0.3))
        correct_signal = _infer_evidence(student_input, agent_output)
        post = update_mastery(prior, correct_signal)

        mastery = dict(row.mastery or {})
        mastery[concept] = round(post, 4)

        history = list(row.scaffold_history or [])
        history.append(
            {
                "timestamp": datetime.now(UTC).isoformat(),
                "concept": concept,
                "scaffold_level": scaffold_level,
                "student_input": student_input[:200],
            }
        )

        row.mastery = mastery
        row.scaffold_history = history
        row.session_count = int(row.session_count or 0) + 1
        row.last_updated = datetime.now(UTC)

        db.add(
            ProvenanceLog(
                learner_state_id=row.id,
                source="memory_write",
                field_name=f"mastery.{concept}",
                old_value=str(prior),
                new_value=str(post),
                confidence=0.7 if correct_signal else 0.5,
            )
        )

        db.commit()

        return {
            "concept": concept,
            "prior": prior,
            "post": post,
            "scaffold_events": len(history),
            "correct_signal": correct_signal,
        }
