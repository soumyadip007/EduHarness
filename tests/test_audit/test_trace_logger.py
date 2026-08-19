from eduharness.audit.trace_logger import TraceLogger
from eduharness.audit.trace_schema import TraceRecord


def test_trace_logger_writes_jsonl(tmp_path) -> None:
    logger = TraceLogger(tmp_path / "trace.jsonl")
    rec = TraceRecord(
        trace_id="t1",
        session_id="s1",
        turn_number=1,
        student_input="hello",
        intent_label="help_seeking",
        adversarial_score=0.0,
        mastery_snapshot={},
        verify_decision="none",
        contract_rule_fired=None,
        agent_output="response",
        post_check_result="pass",
        memory_update={},
        escalation_triggered=False,
        layer_label="agent",
        latency_ms={},
        tokens_used={},
    )
    logger.log(rec)
    lines = (tmp_path / "trace.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert '"trace_id": "t1"' in lines[0]
