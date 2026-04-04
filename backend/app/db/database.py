import logging
import os
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# For SQLite, disable check_same_thread
connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    # Ensure the data directory exists
    db_path = settings.database_url.split("///")[-1]
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    connect_args=connect_args,
)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")

        # Seed demo agent account if not exists
        try:
            from app.models.database_models import Agent
            from app.core.auth import hash_password
            import uuid, json

            async with async_session() as session:
                from sqlalchemy import select
                result = await session.execute(select(Agent).where(Agent.email == "demo@darvix.ai"))
                if not result.scalar_one_or_none():
                    demo = Agent(
                        id=str(uuid.uuid4()),
                        name="Demo Agent",
                        email="demo@darvix.ai",
                        password_hash=hash_password("demo1234"),
                        role="senior",
                        skills=json.dumps(["billing", "technical", "general"]),
                        is_online=True,
                        is_available=True,
                    )
                    session.add(demo)
                    await session.commit()
                    logger.info("Demo agent seeded: demo@darvix.ai / demo1234")
        except Exception as seed_err:
            logger.warning(f"Demo seed skipped: {seed_err}")

    except Exception as e:
        logger.warning(f"Database init failed (app will continue): {e}")
