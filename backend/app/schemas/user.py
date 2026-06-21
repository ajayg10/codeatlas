"""User schemas for API requests and responses."""
import uuid
from datetime import datetime
from pydantic import BaseModel


class GitHubUserSync(BaseModel):
    """Request body when syncing GitHub user after OAuth."""
    github_id: int
    username: str
    email: str | None = None
    avatar_url: str | None = None
    access_token: str | None = None


class UserResponse(BaseModel):
    """Public user response."""
    id: uuid.UUID
    github_id: int
    username: str
    email: str | None
    avatar_url: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
