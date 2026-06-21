"""
Async SQLAlchemy database engine and session management.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


async def get_db():
    """FastAPI dependency that yields an async database session."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Create all tables (for development only; use Alembic in production)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed the MVP default user
    import uuid
    from sqlalchemy import text
    async with async_session_factory() as session:
        default_user_id = "00000000-0000-0000-0000-000000000000"
        await session.execute(
            text("""
                INSERT INTO users (id, github_id, username, email, created_at, updated_at)
                VALUES (:id, '0', 'admin', 'admin@opensource.mentor', NOW(), NOW())
                ON CONFLICT (id) DO NOTHING
            """),
            {"id": uuid.UUID(default_user_id)}
        )
        await session.commit()
