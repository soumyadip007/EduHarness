from eduharness.memory.memory_read import load_state
from eduharness.memory.memory_write import persist_turn
from eduharness.memory.schema import build_session_factory


def test_memory_write_updates_mastery_and_history(tmp_path) -> None:
    sf = build_session_factory(f"sqlite:///{tmp_path/'mem.db'}")
    result = persist_turn(
        sf,
        student_id="s1",
        course_id="c1",
        concept="loops",
        student_input="I understand loops now",
        agent_output="Great work",
        scaffold_level="hint_L1",
    )
    state = load_state(sf, "s1", "c1")
    assert "loops" in state.mastery
    assert len(state.scaffold_history) == 1
    assert result["post"] >= result["prior"]
