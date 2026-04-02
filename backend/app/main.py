"""
DARVIX — AI-Powered Omnichannel Customer Experience Platform
FastAPI Application Entry Point
"""

import logging
import os
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import get_settings
from app.db.database import init_db
from app.api import messages, conversations, agents, websocket
from app.core.message_bus import close_redis

settings = get_settings()
logging.basicConfig(level=logging.DEBUG if settings.debug else logging.INFO)
logger = logging.getLogger(__name__)

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


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

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://darvix-ai.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(messages.router)
app.include_router(conversations.router)
app.include_router(agents.router)
app.include_router(websocket.router)


@app.get("/api/health")
async def health():
    return {"status": "healthy", "name": "DARVIX", "version": "1.0.0"}


# Serve frontend static files (built React app)
if STATIC_DIR.is_dir():
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(request: Request, full_path: str):
        """Serve the React SPA — all non-API routes return index.html."""
        file_path = STATIC_DIR / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(STATIC_DIR / "index.html")
else:
    @app.get("/")
    async def root():
        return {
            "name": "DARVIX",
            "version": "1.0.0",
            "status": "operational",
            "docs": "/docs",
        }
