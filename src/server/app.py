from fastapi import FastAPI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Conversational AI Agent API")

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Server is running"}

# The websocket routes will be attached via the websocket wrapper
