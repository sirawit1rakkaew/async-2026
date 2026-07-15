# light_api.py
# 💡 Smart Lab Lighting System
# Run: uvicorn light_api:app --host 127.0.0.1 --port 8000 --reload

import asyncio
import sys
from copy import deepcopy
from time import ctime

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

# The Windows console defaults to a legacy code page (e.g. cp874) that cannot
# encode emoji / Thai text, which would otherwise crash our log prints.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

app = FastAPI(title="💡 Smart Lab Lighting System")


# ---------------------------------------------------------------------------
# Default configuration for the 4 virtual lights (with simulated HW latency)
# ---------------------------------------------------------------------------
DEFAULT_LIGHTS = {
    "light_1": {"name": "ไฟหน้าประตู (Light 1)", "status": "OFF", "delay": 0.5},
    "light_2": {"name": "ไฟโต๊ะปฏิบัติการ A (Light 2)", "status": "OFF", "delay": 1.2},
    "light_3": {"name": "ไฟโต๊ะปฏิบัติการ B (Light 3)", "status": "OFF", "delay": 2.0},
    "light_4": {"name": "ไฟกระดานหน้าห้อง (Light 4)", "status": "OFF", "delay": 0.8},
}

# Per-student light state: { student_id: { light_id: {...} } }
student_lights: dict[str, dict] = {}

# Per-student list of connected WebSocket clients (the dashboards)
connections: dict[str, list[WebSocket]] = {}


class StatusModel(BaseModel):
    status: str


def get_student_state(student_id: str) -> dict:
    """Return the light state for a student, creating a fresh copy if new."""
    if student_id not in student_lights:
        student_lights[student_id] = deepcopy(DEFAULT_LIGHTS)
    return student_lights[student_id]


async def broadcast(student_id: str) -> None:
    """Push the full, current light payload to every dashboard of a student."""
    payload = get_student_state(student_id)
    dead: list[WebSocket] = []
    for ws in connections.get(student_id, []):
        try:
            await ws.send_json(payload)
        except Exception:
            dead.append(ws)
    # Clean up any clients that dropped mid-broadcast
    for ws in dead:
        connections[student_id].remove(ws)


# ---------------------------------------------------------------------------
# 1. Get All Lights Status
# ---------------------------------------------------------------------------
@app.get("/api/{student_id}/lights")
async def get_lights(student_id: str):
    return get_student_state(student_id)


# ---------------------------------------------------------------------------
# 3. Reset All Lights  (declared before the dynamic {light_id} route)
# ---------------------------------------------------------------------------
@app.delete("/api/{student_id}/lights/reset")
async def reset_lights(student_id: str):
    lights = get_student_state(student_id)
    for light in lights.values():
        light["status"] = "OFF"

    print(f"{ctime()} | [🔄 RESET] Student '{student_id}' reset all lights to OFF")
    await broadcast(student_id)

    return {
        "message": f"รีเซ็ตไฟทุกดวงของนักเรียน {student_id} เป็น OFF เรียบร้อยแล้ว"
    }


# ---------------------------------------------------------------------------
# 2. Control Individual Light (blocks for the simulated hardware delay)
# ---------------------------------------------------------------------------
@app.post("/api/{student_id}/lights/{light_id}")
async def control_light(student_id: str, light_id: str, body: StatusModel):
    lights = get_student_state(student_id)

    if light_id not in lights:
        raise HTTPException(status_code=404, detail="ไม่พบหลอดไฟที่ระบุ")

    new_status = body.status.strip().upper()
    if new_status not in ("ON", "OFF"):
        raise HTTPException(
            status_code=400, detail="สถานะต้องเป็น ON หรือ OFF เท่านั้น"
        )

    delay = lights[light_id]["delay"]
    print(
        f"{ctime()} | [📥 REQUEST] Student '{student_id}' -> {light_id} = {new_status} "
        f"(simulating {delay}s hardware delay...)"
    )

    # Simulate the physical I/O latency of the hardware
    await asyncio.sleep(delay)

    lights[light_id]["status"] = new_status
    print(f"{ctime()} | [✅ DONE] {light_id} is now {new_status}")

    # Notify all dashboards of the new state
    await broadcast(student_id)

    return {
        "student_id": student_id,
        "light_id": light_id,
        "current_status": new_status,
    }


# ---------------------------------------------------------------------------
# WebSocket Channel (for the Web Dashboard frontend)
# ---------------------------------------------------------------------------
@app.websocket("/ws/{student_id}")
async def websocket_endpoint(websocket: WebSocket, student_id: str):
    await websocket.accept()
    connections.setdefault(student_id, []).append(websocket)
    print(f"{ctime()} | [🔌 CONNECTED] Dashboard for student '{student_id}'")

    # Push the current state immediately upon connection
    await websocket.send_json(get_student_state(student_id))

    try:
        while True:
            # Keep the connection alive; we only ever push to the client.
            await websocket.receive_text()
    except WebSocketDisconnect:
        connections[student_id].remove(websocket)
        print(f"{ctime()} | [❌ DISCONNECTED] Dashboard for student '{student_id}'")
