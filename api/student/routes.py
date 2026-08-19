from __future__ import annotations

from pydantic import BaseModel
from fastapi import APIRouter

from eduharness.agent.executor import AgentExecutor, ExecutorInput
from eduharness.agent.llm_client import LLMClient, ModelConfig
from eduharness.agent.tools.code_runner import run_python_code
from eduharness.agent.tools.course_retriever import CourseRetriever
from eduharness.audit.trace_logger import TraceLogger
from eduharness.memory.memory_read import load_state
from eduharness.session.manager import SessionManager

router = APIRouter(prefix="/api/student", tags=["student"])


class MessageRequest(BaseModel):
    session_id: str
    turn_number: int
    message: str
    mode: str = "H0"


class MessageResponse(BaseModel):
    response: str
    mode: str
    scaffold_level: str = "none"


class CodeRunRequest(BaseModel):
    code: str


class CodeRunResponse(BaseModel):
    stdout: str
    stderr: str
    return_code: int


_client = LLMClient(ModelConfig(provider="openai", model_id="gpt-4o-mini"))
_retriever = CourseRetriever("course_content/modules")
_executor = AgentExecutor(_client, _retriever)
_trace_logger = TraceLogger("evaluation/data/results/api_student_trace.jsonl")
_manager = SessionManager(_executor, _trace_logger)


@router.post("/message", response_model=MessageResponse)
def send_message(payload: MessageRequest) -> MessageResponse:
    out = _manager.handle_message(
        session_id=payload.session_id,
        turn_number=payload.turn_number,
        student_input=payload.message,
        mode=payload.mode,
    )
    return MessageResponse(response=out.response, mode=out.mode, scaffold_level=out.scaffold_level)


@router.post("/run-code", response_model=CodeRunResponse)
def run_code(payload: CodeRunRequest) -> CodeRunResponse:
    result = run_python_code(payload.code)
    return CodeRunResponse(stdout=result.stdout, stderr=result.stderr, return_code=result.return_code)


@router.get("/sessions")
def list_sessions() -> dict:
    return {"sessions": [{"session_id": "demo-1", "turns": 6}, {"session_id": "demo-2", "turns": 4}]}


@router.get("/mastery")
def get_mastery(session_id: str = "student-demo-session") -> dict:
    state = load_state(_manager.session_factory, student_id=session_id, course_id="cs101_python")
    if state.mastery:
        return {"mastery": state.mastery}
    return {
        "mastery": {
            "variables": 0.7,
            "conditionals": 0.6,
            "loops": 0.5,
            "functions": 0.4,
            "lists": 0.45,
        }
    }
