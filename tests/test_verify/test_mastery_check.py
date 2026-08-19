from eduharness.verify.mastery_check import estimate_mastery


def test_estimate_mastery_from_concept_mention() -> None:
    snap = estimate_mastery("I am stuck with loops", "configs/concept_maps/python_intro.yaml")
    assert "loops" in snap.concept_mastery
    assert snap.concept_mastery["loops"] >= 0.5
