from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class LearnerState(Base):
    __tablename__ = "learner_state"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[str] = mapped_column(String(128), index=True)
    course_id: Mapped[str] = mapped_column(String(128), index=True)
    mastery: Mapped[dict] = mapped_column(JSON, default=dict)
    misconceptions: Mapped[list] = mapped_column(JSON, default=list)
    scaffold_history: Mapped[list] = mapped_column(JSON, default=list)
    session_count: Mapped[int] = mapped_column(Integer, default=0)
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class TeacherOverride(Base):
    __tablename__ = "teacher_override"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[str] = mapped_column(String(128), index=True)
    course_id: Mapped[str] = mapped_column(String(128), index=True)
    teacher_id: Mapped[str] = mapped_column(String(128), index=True)
    rule_key: Mapped[str] = mapped_column(String(128))
    rule_value: Mapped[str] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class SessionSummary(Base):
    __tablename__ = "session_summary"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[str] = mapped_column(String(128), index=True)
    course_id: Mapped[str] = mapped_column(String(128), index=True)
    summary_text: Mapped[str] = mapped_column(Text)
    turn_count: Mapped[int] = mapped_column(Integer, default=0)
    compacted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class ProvenanceLog(Base):
    __tablename__ = "provenance_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    learner_state_id: Mapped[int | None] = mapped_column(ForeignKey("learner_state.id"), nullable=True)
    source: Mapped[str] = mapped_column(String(64))
    field_name: Mapped[str] = mapped_column(String(128))
    old_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    new_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


def build_session_factory(db_url: str = "sqlite:///eduharness.db"):
    engine = create_engine(db_url, future=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, future=True)
