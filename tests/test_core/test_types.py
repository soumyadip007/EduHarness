from eduharness.core.types import MasterySnapshot


def test_mastery_snapshot_default() -> None:
    snapshot = MasterySnapshot()
    assert snapshot.concept_mastery == {}
    assert snapshot.prerequisites_met is False
