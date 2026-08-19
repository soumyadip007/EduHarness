from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from api.teacher.realtime import broadcaster

router = APIRouter(tags=["teacher-websocket"])


@router.websocket("/ws/escalation")
async def escalation_ws(ws: WebSocket) -> None:
    await broadcaster.connect(ws)
    await ws.send_json({"event": "connected", "message": "Escalation stream ready"})
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        broadcaster.disconnect(ws)
