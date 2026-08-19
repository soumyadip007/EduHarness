from __future__ import annotations


def expected_calibration_error(predicted: list[float], observed: list[int]) -> float:
    if not predicted or not observed or len(predicted) != len(observed):
        return 1.0
    total = len(predicted)
    err = 0.0
    for p, o in zip(predicted, observed):
        err += abs(p - float(o))
    return err / total
