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


class EscalationRecord(Base):
    __tablename__ = "escalation_record"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    escalation_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    session_id: Mapped[str] = mapped_column(String(128), index=True)
    turn_number: Mapped[int] = mapped_column(Integer, default=0)
    priority: Mapped[str] = mapped_column(String(32), default="medium")
    reason: Mapped[str] = mapped_column(String(128), default="")
    status: Mapped[str] = mapped_column(String(32), default="open", index=True)
    owner_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    opened_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    response_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    action_rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    resolution_action: Mapped[str | None] = mapped_column(String(64), nullable=True)


class ChatSession(Base):
    __tablename__ = "chat_session"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    student_id: Mapped[str] = mapped_column(String(128), index=True)
    course_id: Mapped[str] = mapped_column(String(128), default="cs101_python")
    harness_mode: Mapped[str] = mapped_column(String(32), default="H0")
    model_key: Mapped[str] = mapped_column(String(128), default="mid_primary")
    turn_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    last_active_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class ChatTurn(Base):
    __tablename__ = "chat_turn"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(128), index=True)
    turn_number: Mapped[int] = mapped_column(Integer)
    role: Mapped[str] = mapped_column(String(32))
    content: Mapped[str] = mapped_column(Text)
    scaffold_level: Mapped[str] = mapped_column(String(64), default="none")
    model_key: Mapped[str] = mapped_column(String(128), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class PolicyVersion(Base):
    __tablename__ = "policy_version"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    version_tag: Mapped[str] = mapped_column(String(64), index=True)
    yaml_text: Mapped[str] = mapped_column(Text)
    created_by: Mapped[str] = mapped_column(String(128), default="system")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)


class TeacherReply(Base):
    __tablename__ = "teacher_reply"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    escalation_id: Mapped[str] = mapped_column(String(128), index=True)
    session_id: Mapped[str] = mapped_column(String(128), index=True)
    turn_number: Mapped[int] = mapped_column(Integer)
    teacher_id: Mapped[str] = mapped_column(String(128))
    reply_text: Mapped[str] = mapped_column(Text)
    delivered: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class ProgressPlan(Base):
    __tablename__ = "progress_plan"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[str] = mapped_column(String(128), index=True)
    course_id: Mapped[str] = mapped_column(String(128), index=True)
    plan: Mapped[dict] = mapped_column(JSON, default=dict)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class AppSetting(Base):
    __tablename__ = "app_setting"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    value: Mapped[str] = mapped_column(Text)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class ExperimentManifest(Base):
    __tablename__ = "experiment_manifest"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
    seed: Mapped[int] = mapped_column(Integer, default=42)
    model_keys: Mapped[list] = mapped_column(JSON, default=list)
    harness_levels: Mapped[list] = mapped_column(JSON, default=list)
    data_hash: Mapped[str] = mapped_column(String(128), default="")
    config_hash: Mapped[str] = mapped_column(String(128), default="")
    status: Mapped[str] = mapped_column(String(32), default="pending")
    results_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


def build_session_factory(db_url: str = "sqlite:///eduharness.db"):
    engine = create_engine(db_url, future=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, future=True)
