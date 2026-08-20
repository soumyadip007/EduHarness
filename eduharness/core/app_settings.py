from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select

from eduharness.memory.schema import AppSetting


class AppSettingsStore:
    """Persist runtime settings such as active model key."""

    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory

    def get(self, key: str, default: str = "") -> str:
        with self.session_factory() as db:
            row = db.execute(select(AppSetting).where(AppSetting.key == key)).scalar_one_or_none()
            return row.value if row else default

    def set(self, key: str, value: str) -> dict:
        now = datetime.now(UTC)
        with self.session_factory() as db:
            row = db.execute(select(AppSetting).where(AppSetting.key == key)).scalar_one_or_none()
            if row is None:
                row = AppSetting(key=key, value=value, updated_at=now)
                db.add(row)
            else:
                row.value = value
                row.updated_at = now
            db.commit()
            return {"key": key, "value": value, "updated_at": now.isoformat()}
