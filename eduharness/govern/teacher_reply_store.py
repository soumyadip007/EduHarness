from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy import select

from eduharness.memory.schema import TeacherReply


class TeacherReplyStore:
    """Queue teacher-authored replies for delivery on next student turn."""

    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory

    def enqueue(
        self,
        escalation_id: str,
        session_id: str,
        turn_number: int,
        teacher_id: str,
        reply_text: str,
    ) -> dict:
        with self.session_factory() as db:
            row = TeacherReply(
                escalation_id=escalation_id,
                session_id=session_id,
                turn_number=turn_number,
                teacher_id=teacher_id,
                reply_text=reply_text,
                delivered=False,
            )
            db.add(row)
            db.commit()
            db.refresh(row)
            return self._to_dict(row)

    def pop_pending(self, session_id: str) -> dict | None:
        with self.session_factory() as db:
            row = db.execute(
                select(TeacherReply)
                .where(TeacherReply.session_id == session_id, TeacherReply.delivered.is_(False))
                .order_by(TeacherReply.created_at.asc())
            ).scalar_one_or_none()
            if not row:
                return None
            row.delivered = True
            db.commit()
            return self._to_dict(row)

    @staticmethod
    def _to_dict(row: TeacherReply) -> dict:
        return {
            "escalation_id": row.escalation_id,
            "session_id": row.session_id,
            "turn_number": row.turn_number,
            "teacher_id": row.teacher_id,
            "reply_text": row.reply_text,
            "delivered": row.delivered,
            "created_at": row.created_at.isoformat() if row.created_at else None,
        }
