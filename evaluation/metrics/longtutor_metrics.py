from __future__ import annotations


def macro_f1(tp: int, fp: int, fn: int) -> float:
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def history_utilization(score_list: list[float]) -> float:
    if not score_list:
        return 0.0
    return sum(score_list) / len(score_list)
