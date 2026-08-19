from pathlib import Path

from eduharness.govern.patch_log import PatchLog
from eduharness.govern.patch_pipeline import apply_teacher_action


def test_patch_pipeline_updates_contract(tmp_path) -> None:
    contract = tmp_path / "contract.yaml"
    contract.write_text("assessment_modes:\n  practice:\n    hint_cap_per_concept: 5\n", encoding="utf-8")

    log = PatchLog(tmp_path / "patchlog.jsonl")
    res = apply_teacher_action(
        action="patch_rule",
        escalation_id="e1",
        teacher_id="t1",
        contract_path=str(contract),
        patch_log=log,
        patch_rule={"path": "assessment_modes.practice.hint_cap_per_concept", "value": 3},
    )
    assert res["applied"] is True
    assert "patched_path" in res
    assert "hint_cap_per_concept: 3" in contract.read_text(encoding="utf-8")
