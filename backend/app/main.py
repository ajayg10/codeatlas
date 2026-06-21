"""
Open Source Mentor — FastAPI Backend
Main application entry point.
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db
from app.services.cognee_memory import CogneeMemoryService
from app.routers import auth, repositories, ingestion, mentor, feedback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: setup and teardown."""
    # Startup
    logger.info("Starting Open Source Mentor backend...")

    # Initialize database tables (dev mode)
    await init_db()
    logger.info("Database initialized")

    # Connect to Cognee Cloud
    try:
        await CogneeMemoryService.connect()
    except Exception as e:
        logger.warning(f"Cognee connection failed (will retry on use): {e}")

    yield

    # Shutdown
    logger.info("Shutting down...")
    await CogneeMemoryService.disconnect()


app = FastAPI(
    title="Open Source Mentor API",
    description="From first visit to first PR in minutes. Powered by Cognee.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:3000",
        "http://localhost:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(repositories.router)
app.include_router(ingestion.router)
app.include_router(mentor.router)
app.include_router(feedback.router)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "name": "Open Source Mentor API",
        "status": "running",
        "version": "1.0.0",
        "powered_by": "Cognee",
    }


@app.get("/api/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "database": "connected",
        "cognee": "connected" if CogneeMemoryService._connected else "disconnected",
        "llm_provider": settings.LLM_PROVIDER,
    }
