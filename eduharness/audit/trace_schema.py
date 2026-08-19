from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime


@dataclass
class TraceRecord:
    trace_id: str
    session_id: str
    turn_number: int
    student_input: str
    intent_label: str
    adversarial_score: float
    mastery_snapshot: dict[str, float]
    verify_decision: str
    contract_rule_fired: str | None
    agent_output: str
    post_check_result: str
    memory_update: dict
    escalation_triggered: bool
    layer_label: str
    latency_ms: dict[str, int]
    tokens_used: dict[str, int]
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict:
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data
