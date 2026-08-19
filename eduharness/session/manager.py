from __future__ import annotations

from dataclasses import dataclass

from eduharness.agent.executor import AgentExecutor, ExecutorInput
from eduharness.audit.trace_logger import TraceLogger
from eduharness.audit.trace_schema import TraceRecord
from eduharness.session.harness_config import get_harness_config
from eduharness.verify.post_check import post_check_output
from eduharness.verify.verification_gate import run_verification


@dataclass
class SessionResponse:
    response: str
    mode: str


class SessionManager:
    def __init__(self, executor: AgentExecutor, trace_logger: TraceLogger) -> None:
        self.executor = executor
        self.trace_logger = trace_logger

    def handle_message(self, session_id: str, turn_number: int, student_input: str, mode: str = "H0") -> SessionResponse:
        cfg = get_harness_config(mode)
        verify_action = "none"
        verify_reason = ""
        intent_label = "help_seeking"
        adv_score = 0.0
        mastery_snapshot: dict[str, float] = {}
        constraints = ""

        if cfg.enable_verify:
            vr = run_verification(
                student_input=student_input,
                contract_path="configs/contracts/default_contract.yaml",
                concept_map_path="configs/concept_maps/python_intro.yaml",
                assessment_mode="practice",
            )
            verify_action = vr.decision.action
            verify_reason = vr.decision.reason
            intent_label = vr.intent_label
            adv_score = vr.adversarial_score
            mastery_snapshot = vr.mastery.concept_mastery
            constraints = f"Verification action: {verify_action}. Reason: {verify_reason}."

        output = self.executor.run(ExecutorInput(student_input=student_input, constraints=constraints))
        post_result = post_check_output(verify_action, output) if cfg.enable_verify else "pass"
        self.trace_logger.log(
            TraceRecord(
                trace_id=f"{session_id}-{turn_number}",
                session_id=session_id,
                turn_number=turn_number,
                student_input=student_input,
                intent_label=intent_label,
                adversarial_score=adv_score,
                mastery_snapshot=mastery_snapshot,
                verify_decision=verify_action,
                contract_rule_fired=verify_reason or None,
                agent_output=output,
                post_check_result=post_result,
                memory_update={},
                escalation_triggered=False,
                layer_label="verify" if cfg.enable_verify else "agent",
                latency_ms={},
                tokens_used={},
            )
        )
        return SessionResponse(response=output, mode=mode)
