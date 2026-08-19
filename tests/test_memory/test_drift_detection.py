from eduharness.memory.drift_detection import detect_drift


def test_detect_drift_flags_large_gap() -> None:
    out = detect_drift({"loops": 0.9}, {"loops": 0.2}, threshold=0.3)
    assert out["drift_detected"] is True
    assert "loops" in out["concept_deltas"]
