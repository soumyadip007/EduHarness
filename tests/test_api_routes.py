from fastapi.testclient import TestClient

from api.main import app


def test_health() -> None:
    c = TestClient(app)
    r = c.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_auth_login() -> None:
    c = TestClient(app)
    r = c.post("/api/auth/login", json={"username": "alice", "role": "student"})
    assert r.status_code == 200
    data = r.json()
    assert data["role"] == "student"
    assert data["token"].startswith("demo-")


def test_student_message() -> None:
    c = TestClient(app)
    r = c.post(
        "/api/student/message",
        json={"session_id": "s1", "turn_number": 1, "message": "help with loops", "mode": "H2"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["mode"] == "H2"
    assert isinstance(data["response"], str)
    assert "scaffold_level" in data


def test_student_sessions() -> None:
    c = TestClient(app)
    r = c.get("/api/student/sessions")
    assert r.status_code == 200
    assert "sessions" in r.json()


def test_student_run_code() -> None:
    c = TestClient(app)
    r = c.post("/api/student/run-code", json={"code": "print(10+5)"})
    assert r.status_code == 200
    data = r.json()
    assert data["return_code"] == 0
    assert "15" in data["stdout"]


def test_mastery_updates_after_h2_turn() -> None:
    c = TestClient(app)
    session_id = "mastery-check-session"
    c.post(
        "/api/student/message",
        json={"session_id": session_id, "turn_number": 1, "message": "help with loops", "mode": "H2"},
    )
    r = c.get(f"/api/student/mastery?session_id={session_id}")
    assert r.status_code == 200
    mastery = r.json().get("mastery", {})
    assert isinstance(mastery, dict)
    assert "loops" in mastery


def test_teacher_endpoints() -> None:
    c = TestClient(app)
    assert c.get("/api/teacher/queue").status_code == 200
    assert c.get("/api/teacher/students").status_code == 200
    assert c.get("/api/teacher/audit").status_code == 200
    assert c.get("/api/teacher/contract").status_code == 200
    assert c.get("/api/teacher/reports/summary").status_code == 200
