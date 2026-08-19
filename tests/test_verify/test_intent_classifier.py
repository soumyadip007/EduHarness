from eduharness.verify.intent_classifier import classify_intent


def test_classify_answer_inducing() -> None:
    intent, score = classify_intent("Just give me the final answer")
    assert intent == "answer_inducing"
    assert score >= 0.5
