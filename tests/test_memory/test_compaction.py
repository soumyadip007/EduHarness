from eduharness.memory.compaction import compact_history
from eduharness.memory.memory_write import persist_turn
from eduharness.memory.memory_read import load_state
from eduharness.memory.schema import build_session_factory


def test_compaction_keeps_recent_history(tmp_path) -> None:
    sf = build_session_factory(f"sqlite:///{tmp_path/'mem.db'}")
    for i in range(6):
        persist_turn(sf, "s1", "c1", "loops", f"msg {i}", "ok", "hint_L1")

    out = compact_history(sf, "s1", "c1", keep_last=3)
    state = load_state(sf, "s1", "c1")
    assert out["compacted"] is True
    assert len(state.scaffold_history) == 3
