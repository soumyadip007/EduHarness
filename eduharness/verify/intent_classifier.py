from __future__ import annotations

from eduharness.verify.adversarial_detector import adversarial_score


INTENTS = ("help_seeking", "answer_inducing", "off_topic", "exam_sensitive")


def classify_intent(student_input: str) -> tuple[str, float]:
    text = student_input.lower().strip()
    score = adversarial_score(student_input)

    if "exam" in text or "test" in text:
        return "exam_sensitive", max(score, 0.5)

    if any(k in text for k in ("answer", "solution", "full code", "just give")):
        return "answer_inducing", max(score, 0.5)

    if any(k in text for k in ("poem", "resume", "weather", "movie")):
        return "off_topic", score

    return "help_seeking", score
