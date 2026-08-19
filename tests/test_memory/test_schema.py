from sqlalchemy import text

from eduharness.memory.schema import build_session_factory


def test_schema_tables_created(tmp_path) -> None:
    db_path = tmp_path / "mem.db"
    sf = build_session_factory(f"sqlite:///{db_path}")
    with sf() as db:
        tables = db.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        names = {row[0] for row in tables.fetchall()}
    assert {"learner_state", "teacher_override", "session_summary", "provenance_log"}.issubset(names)
