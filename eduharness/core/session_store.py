from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import func, select

from eduharness.memory.schema import ChatSession, ChatTurn, LearnerState


class SessionStore:
    """Persist chat sessions and turns for dynamic student/teacher views."""

    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory

    def record_turn(
        self,
        session_id: str,
        student_id: str,
        turn_number: int,
        student_message: str,
        tutor_response: str,
        mode: str,
        model_key: str,
        scaffold_level: str = "none",
        course_id: str = "cs101_python",
    ) -> None:
        now = datetime.now(UTC)
        with self.session_factory() as db:
            session = db.execute(
                select(ChatSession).where(ChatSession.session_id == session_id)
            ).scalar_one_or_none()
            if session is None:
                session = ChatSession(
                    session_id=session_id,
                    student_id=student_id,
                    course_id=course_id,
                    harness_mode=mode,
                    model_key=model_key,
                    turn_count=0,
                    created_at=now,
                    last_active_at=now,
                )
                db.add(session)
            else:
                session.harness_mode = mode
                session.model_key = model_key
                session.last_active_at = now

            db.add(
                ChatTurn(
                    session_id=session_id,
                    turn_number=turn_number,
                    role="student",
                    content=student_message,
                    scaffold_level="none",
                    model_key=model_key,
                    created_at=now,
                )
            )
            db.add(
                ChatTurn(
                    session_id=session_id,
                    turn_number=turn_number,
                    role="tutor",
                    content=tutor_response,
                    scaffold_level=scaffold_level,
                    model_key=model_key,
                    created_at=now,
                )
            )
            session.turn_count = max(session.turn_count, turn_number)
            db.commit()

    def list_sessions(self, student_id: str | None = None) -> list[dict]:
        with self.session_factory() as db:
            stmt = select(ChatSession).order_by(ChatSession.last_active_at.desc())
            if student_id:
                stmt = stmt.where(ChatSession.student_id == student_id)
            rows = db.execute(stmt).scalars().all()
            return [
                {
                    "session_id": r.session_id,
                    "student_id": r.student_id,
                    "turns": r.turn_count,
                    "mode": r.harness_mode,
                    "model_key": r.model_key,
                    "last_active_at": r.last_active_at.isoformat() if r.last_active_at else None,
                }
                for r in rows
            ]

    def list_students(self) -> list[dict]:
        with self.session_factory() as db:
            learner_rows = db.execute(select(LearnerState)).scalars().all()
            session_counts = dict(
                db.execute(
                    select(ChatSession.student_id, func.count(ChatSession.id)).group_by(ChatSession.student_id)
                ).all()
            )
            students: dict[str, dict] = {}
            for row in learner_rows:
                mastery = row.mastery or {}
                avg = sum(mastery.values()) / len(mastery) if mastery else 0.0
                risk = "high" if avg < 0.4 else ("medium" if avg < 0.6 else "low")
                students[row.student_id] = {
                    "id": row.student_id,
                    "risk": risk,
                    "sessions": int(session_counts.get(row.student_id, row.session_count or 0)),
                    "mastery_avg": round(avg, 3),
                }
            for sid, count in session_counts.items():
                if sid not in students:
                    students[sid] = {"id": sid, "risk": "medium", "sessions": int(count), "mastery_avg": 0.0}
            return list(students.values())

    def get_student_detail(self, student_id: str, escalation_store) -> dict:
        with self.session_factory() as db:
            row = db.execute(
                select(LearnerState).where(LearnerState.student_id == student_id)
            ).scalar_one_or_none()
            mastery = dict(row.mastery) if row and row.mastery else {}
            open_esc = escalation_store.count_open_for_student(student_id)
            return {
                "id": student_id,
                "mastery": mastery,
                "open_escalations": open_esc,
                "session_count": row.session_count if row else 0,
            }
