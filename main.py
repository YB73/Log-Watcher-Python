from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import asyncio
from log_watcher import LogWatcher

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize log watcher
log_watcher = LogWatcher("test_logs/sample.log")
log_watcher.start()

@app.get("/")
async def get_index():
    return FileResponse("static/index.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Send last 10 lines initially
    initial_lines = log_watcher.get_last_n_lines(10)
    for line in initial_lines:
        await websocket.send_text(line.strip())
    
    # Define callback for new lines
    async def send_update(line: str):
        try:
            await websocket.send_text(line.strip())
        except Exception:
            pass
    
    # Register callback
    log_watcher.register_callback(lambda x: asyncio.create_task(send_update(x)))
    
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        log_watcher.unregister_callback(lambda x: asyncio.create_task(send_update(x)))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)