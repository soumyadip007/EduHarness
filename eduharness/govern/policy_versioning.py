from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy import select, update

from eduharness.memory.schema import PolicyVersion


class PolicyVersioning:
    """Version contract YAML with rollback support."""

    def __init__(self, session_factory, contract_path: str | Path) -> None:
        self.session_factory = session_factory
        self.contract_path = Path(contract_path)

    def save_version(self, yaml_text: str, created_by: str = "teacher") -> dict:
        tag = datetime.now(UTC).strftime("v%Y%m%d-%H%M%S")
        with self.session_factory() as db:
            db.execute(update(PolicyVersion).values(is_active=False))
            row = PolicyVersion(
                version_tag=tag,
                yaml_text=yaml_text,
                created_by=created_by,
                is_active=True,
            )
            db.add(row)
            db.commit()
            db.refresh(row)
        self.contract_path.write_text(yaml_text, encoding="utf-8")
        return {"version_tag": tag, "created_by": created_by, "is_active": True}

    def list_versions(self, limit: int = 20) -> list[dict]:
        with self.session_factory() as db:
            rows = db.execute(
                select(PolicyVersion).order_by(PolicyVersion.created_at.desc()).limit(limit)
            ).scalars().all()
            return [
                {
                    "version_tag": r.version_tag,
                    "created_by": r.created_by,
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                    "is_active": r.is_active,
                }
                for r in rows
            ]

    def rollback(self, version_tag: str | None = None) -> dict:
        with self.session_factory() as db:
            if version_tag:
                row = db.execute(
                    select(PolicyVersion).where(PolicyVersion.version_tag == version_tag)
                ).scalar_one_or_none()
            else:
                row = db.execute(
                    select(PolicyVersion)
                    .where(PolicyVersion.is_active.is_(False))
                    .order_by(PolicyVersion.created_at.desc())
                ).scalar_one_or_none()
            if not row:
                return {"rolled_back": False, "message": "No prior version available"}
            db.execute(update(PolicyVersion).values(is_active=False))
            row.is_active = True
            db.commit()
        self.contract_path.write_text(row.yaml_text, encoding="utf-8")
        return {"rolled_back": True, "version_tag": row.version_tag}
