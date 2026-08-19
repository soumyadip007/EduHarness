from __future__ import annotations

from dataclasses import dataclass

from eduharness.agent.llm_client import LLMClient
from eduharness.agent.prompts import BASE_SYSTEM_PROMPT, build_user_prompt
from eduharness.agent.tools.course_retriever import CourseRetriever


@dataclass
class ExecutorInput:
    student_input: str
    constraints: str = ""


class AgentExecutor:
    def __init__(self, llm_client: LLMClient, retriever: CourseRetriever) -> None:
        self.llm_client = llm_client
        self.retriever = retriever

    def run(self, input_data: ExecutorInput) -> str:
        context = self.retriever.retrieve(input_data.student_input)
        user_prompt = build_user_prompt(input_data.student_input, context)
        if input_data.constraints:
            user_prompt += f"\n\nConstraints:\n{input_data.constraints}"
        return self.llm_client.chat(BASE_SYSTEM_PROMPT, user_prompt)
