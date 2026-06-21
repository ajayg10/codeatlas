"""Feedback schemas for the memory improvement lifecycle."""
import uuid
from datetime import datetime
from pydantic import BaseModel
from app.models.feedback import FeedbackRating


class FeedbackCreate(BaseModel):
    """Request body for submitting feedback."""
    feature: str
    query: str
    response_summary: str
    rating: FeedbackRating
    comment: str | None = None


class FeedbackResponse(BaseModel):
    """Response after submitting feedback."""
    id: uuid.UUID
    feature: str
    query: str
    rating: FeedbackRating
    created_at: datetime

    model_config = {"from_attributes": True}
