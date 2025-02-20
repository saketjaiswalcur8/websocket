from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import asyncio
import os
app = FastAPI()
# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")
connected_clients = set()
@app.get("/", response_class=HTMLResponse)
async def get_transcript():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read())
@app.websocket("/anlysis")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for frontend clients to receive real-time transcriptions."""
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")
            for client in connected_clients:
                if client != websocket:  # Ensure we don't send back to sender
                    await client.send_text(data)
    except WebSocketDisconnect:
        print("Frontend client disconnected")
        connected_clients.remove(websocket)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)