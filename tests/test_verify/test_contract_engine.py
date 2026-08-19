from eduharness.core.types import MasterySnapshot
from eduharness.verify.contract_engine import decide_action, load_contract


def test_contract_decide_for_exam_mode() -> None:
    contract = load_contract("configs/contracts/default_contract.yaml")
    decision = decide_action(
        intent="help_seeking",
        mastery=MasterySnapshot(concept_mastery={"loops": 0.9}, prerequisites_met=True),
        assessment_mode="exam",
        contract=contract,
    )
    assert decision.action == "withhold"
