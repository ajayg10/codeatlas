"""Repository schemas for API requests and responses."""
import uuid
from datetime import datetime
from pydantic import BaseModel, HttpUrl
from app.models.repository import RepositoryStatus


class RepositoryCreate(BaseModel):
    """Request body to add a new repository for analysis."""
    github_url: str  # e.g., https://github.com/vercel/next.js
    user_id: str | None = None


class RepositoryResponse(BaseModel):
    """Full repository response."""
    id: uuid.UUID
    github_url: str
    owner: str
    name: str
    description: str | None
    stars: int
    forks: int
    open_issues: int
    language: str | None
    topics: str | None
    default_branch: str
    cognee_dataset_name: str
    status: RepositoryStatus
    ingested_at: datetime | None
    created_at: datetime
    user_id: uuid.UUID

    model_config = {"from_attributes": True}


class RepositoryListItem(BaseModel):
    """Abbreviated repository for list views."""
    id: uuid.UUID
    github_url: str
    owner: str
    name: str
    description: str | None
    stars: int
    forks: int
    language: str | None
    status: RepositoryStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class RepositoryDashboard(BaseModel):
    """Dashboard data for a single repository."""
    id: uuid.UUID
    owner: str
    name: str
    description: str | None
    stars: int
    forks: int
    open_issues: int
    language: str | None
    topics: list[str]
    default_branch: str
    status: RepositoryStatus
    ingested_at: datetime | None
    memory_nodes: int
    memory_relationships: int
    contributor_count: int
    pr_count: int
    discussion_count: int
    technology_stack: list[str]
    contribution_opportunities: int
    recent_activity: list[dict]
