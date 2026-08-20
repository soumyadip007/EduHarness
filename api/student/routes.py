from __future__ import annotations

from pydantic import BaseModel
from fastapi import APIRouter

from api.services import get_active_model_key, get_session_manager
from eduharness.agent.tools.code_runner import run_python_code
from eduharness.memory.memory_read import load_state
from eduharness.pedagogy.progress_plan import generate_progress_plan

router = APIRouter(prefix="/api/student", tags=["student"])


class MessageRequest(BaseModel):
    session_id: str
    turn_number: int
    message: str
    mode: str = "H0"
    model_key: str | None = None


class MessageResponse(BaseModel):
    response: str
    mode: str
    scaffold_level: str = "none"
    model_key: str = ""
    teacher_reply: bool = False


class CodeRunRequest(BaseModel):
    code: str


class CodeRunResponse(BaseModel):
    stdout: str
    stderr: str
    return_code: int


@router.post("/message", response_model=MessageResponse)
def send_message(payload: MessageRequest) -> MessageResponse:
    manager = get_session_manager()
    model_key = payload.model_key or get_active_model_key()
    out = manager.handle_message(
        session_id=payload.session_id,
        turn_number=payload.turn_number,
        student_input=payload.message,
        mode=payload.mode,
        model_key=model_key,
    )
    return MessageResponse(
        response=out.response,
        mode=out.mode,
        scaffold_level=out.scaffold_level,
        model_key=out.model_key,
        teacher_reply=out.teacher_reply,
    )


@router.post("/run-code", response_model=CodeRunResponse)
def run_code(payload: CodeRunRequest) -> CodeRunResponse:
    result = run_python_code(payload.code)
    return CodeRunResponse(stdout=result.stdout, stderr=result.stderr, return_code=result.return_code)


@router.get("/sessions")
def list_sessions(session_id: str | None = None) -> dict:
    manager = get_session_manager()
    sessions = manager.session_store.list_sessions(student_id=session_id)
    return {"sessions": sessions}


@router.get("/mastery")
def get_mastery(session_id: str = "student-demo-session") -> dict:
    manager = get_session_manager()
    state = load_state(manager.session_factory, student_id=session_id, course_id="cs101_python")
    if state.mastery:
        return {"mastery": state.mastery}
    return {"mastery": {}}


@router.get("/progress-plan")
def progress_plan(session_id: str = "student-demo-session") -> dict:
    manager = get_session_manager()
    plan = generate_progress_plan(manager.session_factory, student_id=session_id)
    return {"plan": plan}


@router.get("/questions")
def assigned_questions(session_id: str, count: int = 3) -> dict:
    from eduharness.pedagogy.question_selector import select_questions

    manager = get_session_manager()
    questions = select_questions(manager.session_factory, student_id=session_id, count=count)
    return {"session_id": session_id, "questions": questions}
