from eduharness.simulator.bkt_model import update_mastery


def test_update_mastery_increases_on_correct() -> None:
    prior = 0.3
    post = update_mastery(prior, correct=True)
    assert post > prior
