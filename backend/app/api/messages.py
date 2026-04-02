"""
Message processing pipeline — the core API that channels call.

Flow:
1. Channel adapter parses inbound → normalized message
2. Customer identity resolution
3. Find or create conversation
4. AI analysis pipeline
5. Routing decision
6. Execute (auto-respond, suggest, or escalate)
"""

import uuid
import logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.database_models import (
    Conversation, Message, AIDecisionLog,
    ChannelType, ConversationStatus, MessageSender,
)
from app.models.schemas import InboundMessage, MessageResponse, AIAnalysis
from app.services.ai.engine import analyze_message, generate_response
from app.services.ai.knowledge_base import search_knowledge_base
from app.services.customer.identity import resolve_customer, get_customer_context, get_conversation_history
from app.services.routing.router import route_conversation
from app.services.channels.adapters import get_adapter
from app.core.message_bus import publish_event
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()
router = APIRouter(prefix="/api/messages", tags=["messages"])


@router.post("/inbound/{channel}", response_model=MessageResponse)
async def handle_inbound_message(
    channel: ChannelType,
    payload: dict,
    db: AsyncSession = Depends(get_db),
):
    """
    Universal inbound message endpoint.
    Each channel sends raw payload; adapter normalizes it.
    """
    # 1. Parse via channel adapter
    adapter = get_adapter(channel)
    message = await adapter.parse_inbound(payload)

    # 2. Resolve customer identity
    customer = await resolve_customer(
        db, channel, message.customer_identifier,
        name=message.metadata.get("profile_name"),
    )

    # 3. Find active conversation or create new
    conversation = await _find_or_create_conversation(db, customer.id, channel)

    # 4. Store inbound message
    db_message = Message(
        id=uuid.uuid4(),
        conversation_id=conversation.id,
        sender=MessageSender.CUSTOMER,
        sender_id=customer.id,
        channel=channel,
        content=message.content,
        content_type=message.content_type,
    )
    db.add(db_message)
    await db.flush()

    # 5. AI analysis pipeline
    customer_context = await get_customer_context(db, customer.id)
    conv_history = await get_conversation_history(db, conversation.id)

    analysis = await analyze_message(
        message_content=message.content,
        customer_context=customer_context,
        conversation_history=conv_history,
    )

    # Update message with AI analysis
    db_message.ai_intent = analysis.intent
    db_message.ai_confidence = analysis.intent_confidence
    db_message.ai_sentiment = analysis.sentiment_score

    # Update conversation
    conversation.intent = analysis.intent
    conversation.intent_confidence = analysis.intent_confidence
    conversation.sentiment_score = analysis.sentiment_score
    conversation.urgency = analysis.urgency

    # 6. Route and act
    routing = await route_conversation(db, conversation, analysis, customer.id)

    if routing.decision == "auto_respond":
        # Generate and send AI response
        kb_results = await search_knowledge_base(message.content)
        response_draft = await generate_response(
            message.content, analysis, customer_context, conv_history, kb_results,
        )

        ai_message = Message(
            id=uuid.uuid4(),
            conversation_id=conversation.id,
            sender=MessageSender.AI,
            channel=channel,
            content=response_draft.response_text,
            ai_confidence=response_draft.confidence,
            ai_suggested=False,  # Not a suggestion — direct auto-response
        )
        db.add(ai_message)

        # Send via channel
        await adapter.send_outbound(message.customer_identifier, response_draft.response_text)
        conversation.ai_auto_resolved = True
        conversation.status = ConversationStatus.WAITING_CUSTOMER

    elif routing.decision in ("assign_agent", "escalate"):
        conversation.agent_id = routing.agent_id
        conversation.status = ConversationStatus.WAITING_AGENT
        if routing.decision == "escalate":
            conversation.status = ConversationStatus.ESCALATED

        # Generate AI suggestion for the agent
        kb_results = await search_knowledge_base(message.content)
        response_draft = await generate_response(
            message.content, analysis, customer_context, conv_history, kb_results,
        )

        suggestion = Message(
            id=uuid.uuid4(),
            conversation_id=conversation.id,
            sender=MessageSender.AI,
            channel=channel,
            content=response_draft.response_text,
            ai_confidence=response_draft.confidence,
            ai_suggested=True,
        )
        db.add(suggestion)

        # Notify agent via message bus
        await publish_event("events.agent_notifications", {
            "type": "new_conversation",
            "agent_id": str(routing.agent_id) if routing.agent_id else None,
            "conversation_id": str(conversation.id),
            "customer_name": customer.name,
            "intent": analysis.intent,
            "urgency": analysis.urgency,
            "sentiment": analysis.sentiment_label,
        })

    # Log AI decision
    decision_log = AIDecisionLog(
        id=uuid.uuid4(),
        conversation_id=conversation.id,
        message_id=db_message.id,
        decision_type=routing.decision,
        intent=analysis.intent,
        confidence=analysis.intent_confidence,
        sentiment=analysis.sentiment_score,
        urgency=analysis.urgency,
        action_taken=routing.decision,
        reasoning=routing.reason,
    )
    db.add(decision_log)

    return MessageResponse(
        id=db_message.id,
        conversation_id=conversation.id,
        sender=MessageSender.CUSTOMER,
        channel=channel,
        content=message.content,
        content_type=message.content_type,
        ai_confidence=analysis.intent_confidence,
        ai_intent=analysis.intent,
        ai_sentiment=analysis.sentiment_score,
        ai_suggested=False,
        created_at=db_message.created_at,
    )


@router.post("/agent-send/{conversation_id}", response_model=MessageResponse)
async def agent_send_message(
    conversation_id: uuid.UUID,
    body: dict,
    db: AsyncSession = Depends(get_db),
):
    """Agent sends a message in a conversation."""
    conversation = await db.get(Conversation, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    agent_id = body.get("agent_id")
    content = body.get("content", "")

    msg = Message(
        id=uuid.uuid4(),
        conversation_id=conversation_id,
        sender=MessageSender.AGENT,
        sender_id=uuid.UUID(agent_id) if agent_id else None,
        channel=conversation.channel,
        content=content,
    )
    db.add(msg)

    conversation.status = ConversationStatus.WAITING_CUSTOMER

    # Send via channel adapter
    customer = await db.get(
        __import__("app.models.database_models", fromlist=["Customer"]).Customer,
        conversation.customer_id,
    )
    if customer:
        adapter = get_adapter(conversation.channel)
        identifier = customer.phone or customer.email or ""
        await adapter.send_outbound(identifier, content)

    return MessageResponse(
        id=msg.id,
        conversation_id=conversation_id,
        sender=MessageSender.AGENT,
        channel=conversation.channel,
        content=content,
        content_type="text",
        ai_confidence=None,
        ai_intent=None,
        ai_sentiment=None,
        ai_suggested=False,
        created_at=msg.created_at,
    )


async def _find_or_create_conversation(
    db: AsyncSession,
    customer_id: uuid.UUID,
    channel: ChannelType,
) -> Conversation:
    """Find an active conversation for this customer or create a new one."""
    result = await db.execute(
        select(Conversation).where(
            Conversation.customer_id == customer_id,
            Conversation.status.in_([
                ConversationStatus.ACTIVE,
                ConversationStatus.WAITING_AGENT,
                ConversationStatus.WAITING_CUSTOMER,
            ]),
        ).order_by(Conversation.updated_at.desc())
    )
    existing = result.scalar_one_or_none()

    if existing:
        existing.updated_at = datetime.utcnow()
        # If customer comes from a different channel, note the switch
        if existing.channel != channel:
            logger.info(
                f"Customer {customer_id} switched from {existing.channel} to {channel}"
            )
        return existing

    conversation = Conversation(
        id=uuid.uuid4(),
        customer_id=customer_id,
        channel=channel,
        status=ConversationStatus.ACTIVE,
    )
    db.add(conversation)
    await db.flush()
    return conversation
