from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI(title="Chat Bot Widget Backend")


@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            # Echo back for now; replace with real logic later.
            await websocket.send_text(message)
    except WebSocketDisconnect:
        # Client disconnected; nothing to clean up for now.
        return
