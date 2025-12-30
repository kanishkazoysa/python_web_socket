from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List

app = FastAPI()

# Store active WebSocket connections
active_connections: List[WebSocket] = []

# Regular HTTP endpoint
@app.get("/")
async def get():
    return {"message": "FastAPI WebSocket Server is running!"}

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Accept the connection
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            print(f"Received: {data}")
            
            # Send message back to client
            await websocket.send_text(f"Server received: {data}")
            
            # Broadcast to all connected clients
            for connection in active_connections:
                if connection != websocket:
                    await connection.send_text(f"Broadcast: {data}")
                    
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print("Client disconnected")

# Test page with WebSocket client
@app.get("/test", response_class=HTMLResponse)
async def test_page():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>WebSocket Test</title>
        </head>
        <body>
            <h1>WebSocket Test Client</h1>
            <input id="messageInput" type="text" placeholder="Type a message">
            <button onclick="sendMessage()">Send</button>
            <div id="messages"></div>
            
            <script>
                const ws = new WebSocket("ws://localhost:8000/ws");
                
                ws.onmessage = function(event) {
                    const messages = document.getElementById('messages');
                    const message = document.createElement('div');
                    message.textContent = event.data;
                    messages.appendChild(message);
                };
                
                function sendMessage() {
                    const input = document.getElementById('messageInput');
                    ws.send(input.value);
                    input.value = '';
                }
                
                ws.onopen = function() {
                    console.log("Connected to WebSocket");
                };
                
                ws.onclose = function() {
                    console.log("Disconnected from WebSocket");
                };
            </script>
        </body>
    </html>
    """