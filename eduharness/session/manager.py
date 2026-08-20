from __future__ import annotations

from dataclasses import dataclass

from eduharness.agent.executor import AgentExecutor, ExecutorInput
from eduharness.agent.tools.course_retriever import CourseRetriever
from eduharness.audit.trace_logger import TraceLogger
from eduharness.audit.trace_schema import TraceRecord
from eduharness.core.model_registry import get_model_registry
from eduharness.core.session_store import SessionStore
from eduharness.govern.escalation_store import EscalationStore
from eduharness.govern.evidence_packet import build_evidence_packet
from eduharness.govern.fallback import fallback_response
from eduharness.govern.teacher_reply_store import TeacherReplyStore
from eduharness.memory.memory_read import format_state_for_context, load_state
from eduharness.memory.memory_write import persist_turn
from eduharness.memory.schema import build_session_factory
from eduharness.session.harness_config import get_harness_config
from eduharness.verify.post_check import post_check_output
from eduharness.verify.adversarial_detector import adversarial_score as raw_adversarial_score
from eduharness.verify.verification_gate import run_verification


@dataclass
class SessionResponse:
    response: str
    mode: str
    scaffold_level: str = "none"
    model_key: str = ""
    teacher_reply: bool = False


class SessionManager:
    def __init__(
        self,
        executor: AgentExecutor | None = None,
        trace_logger: TraceLogger | None = None,
        model_key: str | None = None,
    ) -> None:
        self.session_factory = build_session_factory("sqlite:///eduharness.db")
        self.registry = get_model_registry()
        self.model_key = self.registry.get_active_key(model_key)
        self.client = self.registry.get_client(self.model_key)
        retriever = CourseRetriever("course_content/modules")
        self.executor = executor or AgentExecutor(self.client, retriever)
        self.trace_logger = trace_logger or TraceLogger("evaluation/data/results/api_student_trace.jsonl")
        self.escalation_store = EscalationStore(self.session_factory)
        self.session_store = SessionStore(self.session_factory)
        self.teacher_reply_store = TeacherReplyStore(self.session_factory)

    def set_model_key(self, model_key: str) -> None:
        self.registry.validate_key(model_key)
        self.model_key = model_key
        self.client = self.registry.get_client(model_key)
        self.executor = AgentExecutor(self.client, self.executor.retriever)

    @staticmethod
    def _infer_concept(text: str) -> str:
        t = text.lower()
        for concept in ("variables", "conditionals", "loops", "functions", "lists"):
            if concept in t:
                return concept
        return "loops"

    def handle_message(
        self,
        session_id: str,
        turn_number: int,
        student_input: str,
        mode: str = "H0",
        model_key: str | None = None,
    ) -> SessionResponse:
        if model_key and model_key != self.model_key:
            self.set_model_key(model_key)

        pending = self.teacher_reply_store.pop_pending(session_id)
        if pending:
            reply = pending["reply_text"]
            self._record_turn(session_id, turn_number, student_input, reply, mode, "teacher_rewrite")
            model_meta = self.registry.metadata(self.model_key)
            self.trace_logger.log(
                TraceRecord(
                    trace_id=f"{session_id}-{turn_number}",
                    session_id=session_id,
                    turn_number=turn_number,
                    student_input=student_input,
                    intent_label="teacher_reply",
                    adversarial_score=0.0,
                    mastery_snapshot={},
                    verify_decision="teacher_rewrite",
                    contract_rule_fired="teacher_reply_delivery",
                    agent_output=reply,
                    post_check_result="pass",
                    memory_update={},
                    escalation_triggered=False,
                    layer_label="govern",
                    latency_ms={"total": 0},
                    tokens_used={},
                    model_key=model_meta["model_key"],
                    model_id=model_meta["model_id"],
                    model_provider=model_meta["provider"],
                )
            )
            return SessionResponse(
                response=reply,
                mode=mode,
                scaffold_level="teacher_rewrite",
                model_key=self.model_key,
                teacher_reply=True,
            )

        cfg = get_harness_config(mode)
        verify_action = "none"
        verify_reason = ""
        intent_label = "help_seeking"
        adv_score = 0.0
        mastery_snapshot: dict[str, float] = {}
        constraints = ""
        memory_update: dict = {}
        escalated = False

        if cfg.enable_memory:
            state = load_state(self.session_factory, student_id=session_id, course_id="cs101_python")
            constraints += "\n\nLearner state:\n" + format_state_for_context(state)

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
        elif cfg.enable_govern:
            adv_score = raw_adversarial_score(student_input)
            intent_label = "answer_inducing" if adv_score >= 0.5 else "help_seeking"

        output = self.executor.run(ExecutorInput(student_input=student_input, constraints=constraints))
        post_result = post_check_output(verify_action, output) if cfg.enable_verify else "pass"
        call_meta = getattr(self.client, "last_call_metadata", {}) or {}

        if cfg.enable_govern and (
            adv_score >= 0.5
            or post_result in {"block", "rewrite"}
            or verify_action in {"withhold", "escalate"}
        ):
            evidence = build_evidence_packet(
                session_id=session_id,
                turn_number=turn_number,
                student_input=student_input,
                mastery_snapshot=mastery_snapshot,
                verify_action=verify_action,
                verify_reason=verify_reason,
                agent_output=output,
            )
            priority = "high" if verify_action in {"withhold", "escalate"} else "medium"
            escalation_id = f"{session_id}-{turn_number}"
            self.escalation_store.push(
                escalation_id=escalation_id,
                session_id=session_id,
                turn_number=turn_number,
                payload=evidence,
                priority=priority,
                reason=verify_reason or "escalation",
            )
            escalated = True
            output = fallback_response("escalated_for_teacher_review")

        if cfg.enable_memory:
            concept = self._infer_concept(student_input)
            memory_update = persist_turn(
                self.session_factory,
                student_id=session_id,
                course_id="cs101_python",
                concept=concept,
                student_input=student_input,
                agent_output=output,
                scaffold_level=verify_action if verify_action != "none" else "hint_L1",
            )

        model_meta = self.registry.metadata(self.model_key)
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
                memory_update=memory_update,
                escalation_triggered=escalated,
                layer_label=(
                    "govern"
                    if cfg.enable_govern and escalated
                    else ("memory" if cfg.enable_memory else ("verify" if cfg.enable_verify else "agent"))
                ),
                latency_ms={"total": call_meta.get("latency_ms", 0)},
                tokens_used=call_meta.get("tokens_used", {}),
                model_key=model_meta["model_key"],
                model_id=model_meta["model_id"],
                model_provider=model_meta["provider"],
            )
        )
        self._record_turn(session_id, turn_number, student_input, output, mode, verify_action)
        return SessionResponse(
            response=output,
            mode=mode,
            scaffold_level=verify_action,
            model_key=self.model_key,
        )

    def _record_turn(
        self,
        session_id: str,
        turn_number: int,
        student_input: str,
        output: str,
        mode: str,
        scaffold_level: str,
    ) -> None:
        self.session_store.record_turn(
            session_id=session_id,
            student_id=session_id,
            turn_number=turn_number,
            student_message=student_input,
            tutor_response=output,
            mode=mode,
            model_key=self.model_key,
            scaffold_level=scaffold_level,
        )
