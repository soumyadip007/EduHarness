from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

TASKS_PATH = Path("evaluation/data/results/e6_annotation_tasks.jsonl")
LABELS = ["agent", "verify", "memory", "govern"]


def load_tasks() -> list[dict]:
    if not TASKS_PATH.exists():
        return []
    return [json.loads(l) for l in TASKS_PATH.read_text(encoding="utf-8").splitlines() if l.strip()]


def save_tasks(tasks: list[dict]) -> None:
    TASKS_PATH.write_text("\n".join(json.dumps(t, ensure_ascii=True) for t in tasks) + "\n", encoding="utf-8")


st.set_page_config(page_title="E6 Annotation", layout="wide")
st.title("E6 Layer Attribution Annotation")

annotator = st.text_input("Annotator ID", value="annotator_1")
tasks = load_tasks()
if not tasks:
    st.warning("No annotation tasks found. Run: python evaluation/e6_trace_annotation.py")
    st.stop()

pending_idx = next((i for i, t in enumerate(tasks) if not t.get("annotator_label")), None)
if pending_idx is None:
    st.success("All tasks are labeled.")
    st.stop()

task = tasks[pending_idx]
trace = task["trace"]

st.subheader(f"Task {task['task_id']} ({pending_idx+1}/{len(tasks)})")
st.json(trace)
label = st.radio("Select primary layer", LABELS, horizontal=True)

if st.button("Save label"):
    tasks[pending_idx]["annotator_label"] = label
    tasks[pending_idx]["annotator_id"] = annotator
    save_tasks(tasks)
    st.rerun()
