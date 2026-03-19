import os
import sys

# Ensure src in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__(__file__)), "..")))

import asyncio
import logging
import yaml
from fastapi import WebSocket, WebSocketDisconnect
from src.server.app import app
from src.streaming.pipeline import StreamingPipeline

logger = logging.getLogger(__name__)

def load_config():
    config_path = os.path.join("configs", "default.yaml")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    return {}

config = load_config()
pipeline = StreamingPipeline(config)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket Client Connected")
    try:
        while True:
            # We receive chunked audio bytes (simulated here as encoded text bytes)
            data = await websocket.receive_bytes()
            
            # Fire and forget / await pipeline output
            async for token in pipeline.process_audio_chunk(data):
                # Send generated tokens sequentially via webosockets to simulate stream
                await websocket.send_text(token)
            
            # Send End-of-turn marker
            await websocket.send_text("[EOT]")
    except WebSocketDisconnect:
        logger.info("WebSocket Client Disconnected")

if __name__ == "__main__":
    import uvicorn
    host = config.get("server", {}).get("host", "0.0.0.0")
    port = config.get("server", {}).get("port", 8000)
    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
