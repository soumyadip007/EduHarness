from __future__ import annotations


def build_evidence_packet(
    session_id: str,
    turn_number: int,
    student_input: str,
    mastery_snapshot: dict[str, float],
    verify_action: str,
    verify_reason: str,
    agent_output: str,
) -> dict:
    return {
        "session_id": session_id,
        "turn_number": turn_number,
        "student_input": student_input,
        "mastery_snapshot": mastery_snapshot,
        "verify_action": verify_action,
        "verify_reason": verify_reason,
        "agent_output": agent_output,
    }
