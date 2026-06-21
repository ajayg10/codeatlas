"""Ingestion schemas for tracking pipeline progress."""
import uuid
from datetime import datetime
from pydantic import BaseModel
from app.models.ingestion_job import IngestionStep, IngestionStatus


class IngestionJobResponse(BaseModel):
    """Single ingestion job step status."""
    id: uuid.UUID
    step: IngestionStep
    status: IngestionStatus
    progress: int
    items_processed: int
    items_total: int
    error_message: str | None
    started_at: datetime | None
    completed_at: datetime | None

    model_config = {"from_attributes": True}


class IngestionProgressEvent(BaseModel):
    """SSE event for real-time ingestion updates."""
    step: str
    status: str
    progress: int
    message: str
    items_processed: int
    items_total: int


class IngestionStatusResponse(BaseModel):
    """Full ingestion status for a repository."""
    repository_id: uuid.UUID
    overall_status: str
    overall_progress: int
    jobs: list[IngestionJobResponse]
