from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select

from eduharness.memory.schema import EscalationRecord


class EscalationStore:
    """Database-backed escalation queue shared by SessionManager and teacher API."""

    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory

    def push(
        self,
        escalation_id: str,
        session_id: str,
        turn_number: int,
        payload: dict,
        priority: str = "medium",
        reason: str = "",
    ) -> dict:
        with self.session_factory() as db:
            existing = db.execute(
                select(EscalationRecord).where(EscalationRecord.escalation_id == escalation_id)
            ).scalar_one_or_none()
            if existing and existing.status == "open":
                return self._to_dict(existing)

            row = EscalationRecord(
                escalation_id=escalation_id,
                session_id=session_id,
                turn_number=turn_number,
                priority=priority,
                reason=reason or payload.get("verify_reason", "escalation"),
                status="open",
                payload=payload,
                opened_at=datetime.now(UTC),
            )
            db.add(row)
            db.commit()
            db.refresh(row)
            return self._to_dict(row)

    def list_open(self, owner_id: str | None = None) -> list[dict]:
        with self.session_factory() as db:
            stmt = select(EscalationRecord).where(EscalationRecord.status == "open")
            if owner_id:
                stmt = stmt.where(EscalationRecord.owner_id == owner_id)
            rows = db.execute(stmt.order_by(EscalationRecord.opened_at.desc())).scalars().all()
            return [self._to_dict(r) for r in rows]

    def get(self, escalation_id: str) -> dict | None:
        with self.session_factory() as db:
            row = db.execute(
                select(EscalationRecord).where(EscalationRecord.escalation_id == escalation_id)
            ).scalar_one_or_none()
            return self._to_dict(row) if row else None

    def assign(self, escalation_id: str, owner_id: str) -> dict | None:
        with self.session_factory() as db:
            row = db.execute(
                select(EscalationRecord).where(EscalationRecord.escalation_id == escalation_id)
            ).scalar_one_or_none()
            if not row:
                return None
            row.owner_id = owner_id
            db.commit()
            db.refresh(row)
            return self._to_dict(row)

    def resolve(
        self,
        escalation_id: str,
        action: str,
        teacher_id: str,
        rationale: str | None = None,
    ) -> dict | None:
        with self.session_factory() as db:
            row = db.execute(
                select(EscalationRecord).where(EscalationRecord.escalation_id == escalation_id)
            ).scalar_one_or_none()
            if not row:
                return None
            now = datetime.now(UTC)
            opened = row.opened_at
            if opened.tzinfo is None:
                opened = opened.replace(tzinfo=UTC)
            row.status = "resolved"
            row.resolved_at = now
            row.response_time_ms = int((now - opened).total_seconds() * 1000)
            row.resolution_action = action
            row.action_rationale = rationale
            if not row.owner_id:
                row.owner_id = teacher_id
            db.commit()
            db.refresh(row)
            return self._to_dict(row)

    def count_open_for_student(self, session_id: str) -> int:
        with self.session_factory() as db:
            rows = db.execute(
                select(EscalationRecord).where(
                    EscalationRecord.session_id == session_id,
                    EscalationRecord.status == "open",
                )
            ).scalars().all()
            return len(rows)

    def kpi_summary(self) -> dict:
        with self.session_factory() as db:
            rows = db.execute(select(EscalationRecord)).scalars().all()
            resolved = [r for r in rows if r.status == "resolved"]
            open_count = len([r for r in rows if r.status == "open"])
            response_times = [r.response_time_ms for r in resolved if r.response_time_ms is not None]
            avg_response_ms = int(sum(response_times) / len(response_times)) if response_times else 0
            patch_success = len(resolved) / len(rows) if rows else 0.0
            return {
                "open_escalations": open_count,
                "total_escalations": len(rows),
                "resolved_escalations": len(resolved),
                "interventions_per_week": len(resolved),
                "patch_success_rate": round(patch_success, 3),
                "avg_response_time_ms": avg_response_ms,
            }

    @staticmethod
    def _to_dict(row: EscalationRecord) -> dict:
        return {
            "escalation_id": row.escalation_id,
            "session_id": row.session_id,
            "turn_number": row.turn_number,
            "priority": row.priority,
            "reason": row.reason,
            "status": row.status,
            "owner_id": row.owner_id,
            "payload": row.payload or {},
            "opened_at": row.opened_at.isoformat() if row.opened_at else None,
            "resolved_at": row.resolved_at.isoformat() if row.resolved_at else None,
            "response_time_ms": row.response_time_ms,
            "action_rationale": row.action_rationale,
            "resolution_action": row.resolution_action,
            "student_input": (row.payload or {}).get("student_input", ""),
            "verify_action": (row.payload or {}).get("verify_action", ""),
        }
