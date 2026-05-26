from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import cv2
import json
import asyncio
import logging
from typing import List

# We would ideally pass the global instances of Comms, Camera, and State
# to this app, but for starter-code simplicity, we'll mock the integration 
# or assume global access if imported carefully.

app = FastAPI()
app.mount("/static", StaticFiles(directory="api/static", html=True), name="static")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Global mock for telemetry (in a real app, import the Comms/State manager)
telemetry_data = {
    "battery": 12.1,
    "front_sonar": 100,
    "rear_sonar": 80,
    "pi_temp": 45.0,
    "state": "IDLE"
}

@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Broadcast telemetry every 1 second
            await websocket.send_text(json.dumps(telemetry_data))
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.websocket("/ws/control")
async def websocket_control(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            cmd = json.loads(data)
            logging.info(f"Received manual control: {cmd}")
            # Example: cmd = {"action": "drive", "direction": "forward"}
            # Here you would call nav.manual_drive(cmd["direction"])
    except WebSocketDisconnect:
        pass

def generate_video_stream():
    # Mock camera stream for dashboard demo
    cap = cv2.VideoCapture(0) # Adjust index if needed
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Encode to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
            
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(generate_video_stream(), media_type="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
