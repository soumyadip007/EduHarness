from __future__ import annotations

from pydantic import BaseModel
from fastapi import APIRouter

from eduharness.agent.executor import AgentExecutor, ExecutorInput
from eduharness.agent.llm_client import LLMClient, ModelConfig
from eduharness.agent.tools.course_retriever import CourseRetriever
from eduharness.audit.trace_logger import TraceLogger
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
    return MessageResponse(response=out.response, mode=out.mode)


@router.get("/sessions")
def list_sessions() -> dict:
    return {"sessions": [{"session_id": "demo-1", "turns": 6}, {"session_id": "demo-2", "turns": 4}]}


@router.get("/mastery")
def get_mastery() -> dict:
    return {
        "mastery": {
            "variables": 0.7,
            "conditionals": 0.6,
            "loops": 0.5,
            "functions": 0.4,
            "lists": 0.45,
        }
    }
