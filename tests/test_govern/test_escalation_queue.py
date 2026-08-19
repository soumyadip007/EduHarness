from eduharness.govern.escalation_queue import EscalationQueue


def test_escalation_queue_priority_order() -> None:
    q = EscalationQueue()
    q.push("e-low", {"x": 1}, priority="low")
    q.push("e-high", {"x": 2}, priority="high")

    first = q.pop()
    assert first is not None
    assert first.escalation_id == "e-high"
