from eduharness.govern.fallback import fallback_response


def test_fallback_response_contains_reason() -> None:
    msg = fallback_response("teacher_unavailable")
    assert "fallback" in msg.lower()
    assert "teacher_unavailable" in msg
