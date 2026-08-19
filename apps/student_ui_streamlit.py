from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from eduharness.agent.executor import AgentExecutor, ExecutorInput
from eduharness.agent.llm_client import LLMClient, ModelConfig
from eduharness.agent.tools.course_retriever import CourseRetriever

st.set_page_config(page_title="EduHarness Student UI", layout="wide")
st.title("EduHarness Student Tutor")
st.caption("Prototype chat + session history UI")

history_path = Path("evaluation/data/results/student_ui_history.json")
if "messages" not in st.session_state:
    st.session_state.messages = json.loads(history_path.read_text(encoding="utf-8")) if history_path.exists() else []

left, right = st.columns([3, 1])
with left:
    for m in st.session_state.messages:
        role = "🧑 Student" if m["role"] == "student" else "🤖 Tutor"
        st.markdown(f"**{role}:** {m['text']}")

    text = st.text_area("Ask your question", height=120)
    if st.button("Send") and text.strip():
        client = LLMClient(ModelConfig(provider="openai", model_id="gpt-4o-mini"))
        retriever = CourseRetriever("course_content/modules")
        executor = AgentExecutor(client, retriever)
        st.session_state.messages.append({"role": "student", "text": text.strip()})
        st.session_state.messages.append({"role": "tutor", "text": executor.run(ExecutorInput(student_input=text.strip()))})
        history_path.parent.mkdir(parents=True, exist_ok=True)
        history_path.write_text(json.dumps(st.session_state.messages, indent=2), encoding="utf-8")
        st.rerun()

with right:
    st.subheader("Session History")
    st.write(f"Messages: {len(st.session_state.messages)}")
    if st.button("Clear History"):
        st.session_state.messages = []
        if history_path.exists():
            history_path.unlink()
        st.rerun()
