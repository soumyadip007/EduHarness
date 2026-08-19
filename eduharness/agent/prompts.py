BASE_SYSTEM_PROMPT = """You are a Python tutor.
Guide students with hints and scaffolding.
Do not immediately reveal full solutions unless explicitly allowed.
"""


def build_user_prompt(student_input: str, retrieved_context: str | None = None) -> str:
    if retrieved_context:
        return f"Context:\n{retrieved_context}\n\nStudent: {student_input}"
    return f"Student: {student_input}"
