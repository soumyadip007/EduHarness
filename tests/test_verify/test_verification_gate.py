from eduharness.verify.verification_gate import run_verification


def test_run_verification_returns_decision() -> None:
    result = run_verification(
        student_input="Can you explain loops?",
        contract_path="configs/contracts/default_contract.yaml",
        concept_map_path="configs/concept_maps/python_intro.yaml",
    )
    assert result.intent_label in {"help_seeking", "answer_inducing", "exam_sensitive", "off_topic"}
    assert result.decision.action
