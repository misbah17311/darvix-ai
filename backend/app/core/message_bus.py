"""
Redis message bus for real-time event streaming.
"""

import json
import logging
from typing import AsyncGenerator
import redis.asyncio as redis
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

_redis: redis.Redis | None = None


async def get_redis() -> redis.Redis:
    global _redis
    if _redis is None:
        _redis = redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


async def publish_event(stream: str, data: dict):
    """Publish an event to a Redis stream."""
    r = await get_redis()
    await r.xadd(stream, {"data": json.dumps(data)})
    logger.debug(f"Published to {stream}: {data.get('type', 'unknown')}")


async def subscribe_events(stream: str, group: str, consumer: str) -> AsyncGenerator[dict, None]:
    """Subscribe to events from a Redis stream using consumer groups."""
    r = await get_redis()

    # Create consumer group if not exists
    try:
        await r.xgroup_create(stream, group, id="0", mkstream=True)
    except redis.ResponseError:
        pass  # Group already exists

    while True:
        try:
            messages = await r.xreadgroup(group, consumer, {stream: ">"}, count=10, block=5000)
            for _, message_list in messages:
                for msg_id, msg_data in message_list:
                    data = json.loads(msg_data.get("data", "{}"))
                    yield data
                    await r.xack(stream, group, msg_id)
        except Exception as e:
            logger.error(f"Stream read error: {e}")
            break


async def close_redis():
    global _redis
    if _redis:
        await _redis.close()
        _redis = None
