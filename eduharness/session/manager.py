from __future__ import annotations

from dataclasses import dataclass

from eduharness.agent.executor import AgentExecutor, ExecutorInput
from eduharness.audit.trace_logger import TraceLogger
from eduharness.audit.trace_schema import TraceRecord


@dataclass
class SessionResponse:
    response: str
    mode: str


class SessionManager:
    def __init__(self, executor: AgentExecutor, trace_logger: TraceLogger) -> None:
        self.executor = executor
        self.trace_logger = trace_logger

    def handle_message(self, session_id: str, turn_number: int, student_input: str, mode: str = "H0") -> SessionResponse:
        output = self.executor.run(ExecutorInput(student_input=student_input))
        self.trace_logger.log(
            TraceRecord(
                trace_id=f"{session_id}-{turn_number}",
                session_id=session_id,
                turn_number=turn_number,
                student_input=student_input,
                intent_label="help_seeking",
                adversarial_score=0.0,
                mastery_snapshot={},
                verify_decision="none",
                contract_rule_fired=None,
                agent_output=output,
                post_check_result="pass",
                memory_update={},
                escalation_triggered=False,
                layer_label="agent",
                latency_ms={},
                tokens_used={},
            )
        )
        return SessionResponse(response=output, mode=mode)
