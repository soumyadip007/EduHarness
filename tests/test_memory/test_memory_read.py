from eduharness.memory.memory_read import format_state_for_context, load_state
from eduharness.memory.schema import LearnerState, build_session_factory


def test_memory_read_and_format(tmp_path) -> None:
    sf = build_session_factory(f"sqlite:///{tmp_path/'mem.db'}")
    with sf() as db:
        db.add(LearnerState(student_id="s1", course_id="c1", mastery={"loops": 0.5}, misconceptions=[], scaffold_history=[]))
        db.commit()

    state = load_state(sf, "s1", "c1")
    text = format_state_for_context(state)
    assert "loops" in text
