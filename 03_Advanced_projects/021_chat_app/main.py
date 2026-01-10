from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List

app = FastAPI()

# 1. The Manager: It keeps a list of everyone currently in the chat
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        # This sends the message to EVERYONE in the list
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# 2. Serve the Chat Page
@app.get("/")
async def get():
    with open("index.html", "r") as f:
        return HTMLResponse(content=f.read())

# 3. The WebSocket Pipe
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            # Wait for a message from this specific user
            data = await websocket.receive_text()
            # Send that message to everyone else
            await manager.broadcast(f"User #{client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"User #{client_id} has left the chat.")