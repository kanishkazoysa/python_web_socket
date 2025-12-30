# FastAPI WebSocket Chat Server

A real-time WebSocket server built with FastAPI for chat applications.

## Features

- ✅ Real-time bidirectional communication using WebSockets
- ✅ Multiple client connections support
- ✅ Message broadcasting to all connected clients
- ✅ Built-in test client interface
- ✅ RESTful API endpoints

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository:**
```bash
git clone <your-repository-url>
cd phython-web-socket
```

2. **Create a virtual environment:**
```bash
python3 -m venv venv
```

3. **Activate the virtual environment:**

On Linux/Mac:
```bash
source venv/bin/activate
```

On Windows:
```bash
venv\Scripts\activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Running the Server

1. **Start the server:**
```bash
uvicorn main:app --reload
```

2. **The server will start on:** `http://127.0.0.1:8000`

## API Endpoints

### HTTP Endpoints

- `GET /` - Health check endpoint
  - Returns: `{"message": "FastAPI WebSocket Server is running!"}`

- `GET /test` - Built-in WebSocket test client
  - Open in browser to test WebSocket functionality

### WebSocket Endpoint

- `WS /ws` - WebSocket connection endpoint
  - Accepts client connections
  - Receives and broadcasts messages to all connected clients

## Usage Example

### Using the Test Client

1. Open your browser
2. Navigate to `http://127.0.0.1:8000/test`
3. Type a message and click "Send"
4. Open multiple browser tabs to see broadcast functionality

### Connecting from JavaScript
```javascript
const ws = new WebSocket("ws://localhost:8000/ws");

ws.onopen = () => {
    console.log("Connected to server");
    ws.send("Hello Server!");
};

ws.onmessage = (event) => {
    console.log("Received:", event.data);
};

ws.onclose = () => {
    console.log("Disconnected from server");
};
```

### Connecting from Python
```python
import asyncio
import websockets

async def connect():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello Server!")
        response = await websocket.recv()
        print(f"Received: {response}")

asyncio.run(connect())
```

## Project Structure
```
phython-web-socket/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
└── venv/               # Virtual environment (not in git)
```

## Dependencies

- **FastAPI** - Modern web framework for building APIs
- **Uvicorn** - ASGI server for running FastAPI
- **Websockets** - WebSocket protocol implementation

## Development

To contribute or modify:

1. Make your changes to `main.py`
2. The server will auto-reload (if using `--reload` flag)
3. Test your changes using the `/test` endpoint

## Troubleshooting

### Server won't start
- Make sure virtual environment is activated
- Check if port 8000 is already in use
- Verify all dependencies are installed: `pip list`

### WebSocket connection fails
- Ensure server is running
- Check browser console for errors
- Verify WebSocket URL is correct (`ws://` not `http://`)

## License

MIT License

## Author

Your Name

## Support

For issues or questions, please open an issue on GitHub.
```

## Issue 3: Create/Update .gitignore

You should also have a `.gitignore` file to avoid committing unnecessary files:

**Create `.gitignore` file:**
```
# Virtual Environment
venv/
env/
ENV/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment variables
.env
.env.local