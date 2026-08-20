from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.auth.routes import router as auth_router
from api.config.routes import router as config_router
from api.teacher.websocket import router as teacher_ws_router
from api.student.routes import router as student_router
from api.teacher.routes import router as teacher_router
from api.researcher.routes import router as researcher_router

app = FastAPI(title="EduHarness API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(config_router)
app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(researcher_router)
app.include_router(teacher_ws_router)
