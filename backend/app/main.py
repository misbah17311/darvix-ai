"""
DARVIX — AI-Powered Omnichannel Customer Experience Platform
FastAPI Application Entry Point
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db.database import init_db
from app.api import messages, conversations, agents, websocket
from app.core.message_bus import close_redis

settings = get_settings()
logging.basicConfig(level=logging.DEBUG if settings.debug else logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting DARVIX platform...")
    await init_db()
    logger.info("Database initialized")
    yield
    await close_redis()
    logger.info("DARVIX platform shut down")


app = FastAPI(
    title="DARVIX",
    description="AI-Powered Omnichannel Customer Experience Platform",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(messages.router)
app.include_router(conversations.router)
app.include_router(agents.router)
app.include_router(websocket.router)


@app.get("/")
async def root():
    return {
        "name": "DARVIX",
        "version": "1.0.0",
        "status": "operational",
        "description": "AI-Powered Omnichannel Customer Experience Platform",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
