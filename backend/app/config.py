from pydantic_settings import BaseSettings
from pydantic import model_validator
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "DARVIX"
    debug: bool = False

    # Database — defaults to local SQLite so it works without external DB
    database_url: str = "sqlite+aiosqlite:///./data/darvix.db"

    @model_validator(mode="after")
    def fix_database_url(self):
        """Render provides postgres:// URLs; convert for asyncpg."""
        url = self.database_url
        if url.startswith("postgres://"):
            self.database_url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://") and "+asyncpg" not in url:
            self.database_url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return self

    # Redis
    redis_url: str = "redis://localhost:6379"

    # OpenAI
    openai_api_key: str = ""
    openai_model_heavy: str = "gpt-4o"
    openai_model_light: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"

    # AI Thresholds
    ai_auto_respond_confidence: float = 0.85
    ai_suggest_confidence: float = 0.70
    ai_urgency_escalation_threshold: int = 4

    # ChromaDB
    chroma_persist_dir: str = "./data/chroma"

    # Auth
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 480

    # WebSocket
    ws_heartbeat_interval: int = 30

    model_config = {"env_file": ".env", "env_prefix": "DARVIX_"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
