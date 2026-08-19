from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class MasterySnapshot:
    concept_mastery: dict[str, float] = field(default_factory=dict)
    prerequisites_met: bool = False


@dataclass
class Turn:
    session_id: str
    turn_number: int
    student_input: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class VerifyDecision:
    action: str
    reason: str


@dataclass
class TraceRecord:
    session_id: str
    turn_number: int
    intent_label: str
    verify_action: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
