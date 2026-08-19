from __future__ import annotations

from fastapi import APIRouter, WebSocket

router = APIRouter(tags=["teacher-websocket"])


@router.websocket("/ws/escalation")
async def escalation_ws(ws: WebSocket) -> None:
    await ws.accept()
    await ws.send_json({"event": "connected", "message": "Escalation stream ready"})
    await ws.close()
