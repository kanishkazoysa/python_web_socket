from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json
import httpx
import asyncio

app = FastAPI()

# Enable CORS for WordPress site
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your WordPress domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active WebSocket connections
active_connections: List[WebSocket] = []

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"Client connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"Client disconnected. Total connections: {len(self.active_connections)}")

    async def send_message(self, message: dict, websocket: WebSocket):
        await websocket.send_text(json.dumps(message))

manager = ConnectionManager()

# Health check endpoint
@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "FastAPI WebSocket Chatbot Backend",
        "active_connections": len(manager.active_connections)
    }

# WebSocket endpoint for chat
@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await manager.connect(websocket)
    
    try:
        while True:
            # Receive message from WordPress frontend
            data = await websocket.receive_text()
            print(f"Received from client: {data}")
            
            try:
                message_data = json.loads(data)
                user_message = message_data.get("message", "")
                api_key = message_data.get("api_key", "")
                
                if not user_message:
                    await manager.send_message({
                        "type": "error",
                        "message": "No message provided"
                    }, websocket)
                    continue
                
                # Send typing indicator
                await manager.send_message({
                    "type": "typing",
                    "typing": True
                }, websocket)
                
                # Call OpenRouter API (Free LLM)
                bot_response = await get_llm_response(user_message, api_key)
                
                # Send typing indicator off
                await manager.send_message({
                    "type": "typing",
                    "typing": False
                }, websocket)
                
                # Send bot response
                await manager.send_message({
                    "type": "message",
                    "message": bot_response,
                    "from": "bot"
                }, websocket)
                
            except json.JSONDecodeError:
                await manager.send_message({
                    "type": "error",
                    "message": "Invalid JSON format"
                }, websocket)
            except Exception as e:
                print(f"Error processing message: {str(e)}")
                await manager.send_message({
                    "type": "error",
                    "message": f"Error: {str(e)}"
                }, websocket)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        manager.disconnect(websocket)

# Function to call OpenRouter API
async def get_llm_response(user_message: str, api_key: str) -> str:
    """
    Call OpenRouter API with the user's message
    """
    if not api_key:
        return "Please configure the API key in WordPress admin panel."
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant. Answer briefly and clearly. Use plain text only, no markdown formatting. Keep responses concise, maximum 4 sentences."
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "max_tokens": 150
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            
            if response.status_code != 200:
                return f"API Error: {response.status_code}. Please check your API key."
            
            data = response.json()
            bot_message = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            if not bot_message:
                return "I apologize, but I could not generate a response."
            
            return bot_message
            
    except httpx.TimeoutException:
        return "Request timed out. Please try again."
    except Exception as e:
        print(f"LLM API Error: {str(e)}")
        return f"Sorry, I encountered an error: {str(e)}"

# Run with: uvicorn main:app --reload --host 0.0.0.0 --port 8000