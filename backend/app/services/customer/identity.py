"""
Customer Identity Resolution Service.

Resolves customer identity across channels using:
1. Exact match: email, phone
2. Fuzzy match: name + metadata
3. Creates new customer profile if no match found
"""

import uuid
import logging
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.database_models import Customer, Conversation, Message, ChannelType

logger = logging.getLogger(__name__)


async def resolve_customer(
    db: AsyncSession,
    channel: ChannelType,
    identifier: str,
    name: str | None = None,
) -> Customer:
    """
    Resolve or create a customer based on channel identifier.
    WhatsApp/Voice → phone lookup
    Email → email lookup
    WebChat/Social → session-based, try email/phone if provided
    """
    customer = None

    # Try exact match first
    if channel in (ChannelType.WHATSAPP, ChannelType.VOICE):
        customer = await _find_by_phone(db, identifier)
    elif channel == ChannelType.EMAIL:
        customer = await _find_by_email(db, identifier)
    else:
        # Web chat / social — try both
        customer = await _find_by_email(db, identifier) or await _find_by_phone(db, identifier)

    if customer:
        logger.info(f"Customer resolved: {customer.id} via {channel}")
        return customer

    # Create new customer
    customer = Customer(
        id=uuid.uuid4(),
        email=identifier if channel == ChannelType.EMAIL else None,
        phone=identifier if channel in (ChannelType.WHATSAPP, ChannelType.VOICE) else None,
        name=name,
        segment="standard",
    )
    db.add(customer)
    await db.flush()
    logger.info(f"New customer created: {customer.id}")
    return customer


async def get_customer_context(db: AsyncSession, customer_id: uuid.UUID) -> dict:
    """
    Build rich customer context for AI processing.
    Includes profile data, recent conversations, and computed metrics.
    """
    customer = await db.get(Customer, customer_id)
    if not customer:
        return {}

    # Get recent conversations
    result = await db.execute(
        select(Conversation)
        .where(Conversation.customer_id == customer_id)
        .order_by(Conversation.created_at.desc())
        .limit(10)
    )
    recent_conversations = result.scalars().all()

    return {
        "customer_id": str(customer.id),
        "name": customer.name,
        "email": customer.email,
        "segment": customer.segment,
        "lifetime_value": customer.lifetime_value,
        "csat_avg": customer.csat_avg,
        "total_conversations": len(recent_conversations),
        "recent_intents": [c.intent for c in recent_conversations if c.intent],
        "has_open_issues": any(
            c.status in ("active", "waiting_agent", "escalated") for c in recent_conversations
        ),
    }


async def get_conversation_history(
    db: AsyncSession, conversation_id: uuid.UUID
) -> list[dict]:
    """Get message history for a conversation."""
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    )
    messages = result.scalars().all()
    return [
        {
            "sender": msg.sender.value,
            "content": msg.content,
            "channel": msg.channel.value,
            "timestamp": msg.created_at.isoformat(),
        }
        for msg in messages
    ]


async def _find_by_email(db: AsyncSession, email: str) -> Customer | None:
    result = await db.execute(select(Customer).where(Customer.email == email))
    return result.scalar_one_or_none()


async def _find_by_phone(db: AsyncSession, phone: str) -> Customer | None:
    result = await db.execute(select(Customer).where(Customer.phone == phone))
    return result.scalar_one_or_none()
