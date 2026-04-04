"""
Conversation & Dashboard API routes.
"""

import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.database import get_db
from app.models.database_models import Conversation, Message, Customer, Agent, ConversationStatus
from app.models.schemas import (
    ConversationResponse, ConversationDetail, CustomerResponse, DashboardMetrics,
)
from app.core.auth import get_current_agent

router = APIRouter(prefix="/api", tags=["conversations"])


@router.get("/conversations", response_model=list[ConversationResponse])
async def list_conversations(
    status: ConversationStatus | None = None,
    agent_id: str | None = None,
    limit: int = Query(default=50, le=200),
    db: AsyncSession = Depends(get_db),
):
    """List conversations with optional filters."""
    query = select(Conversation).order_by(Conversation.updated_at.desc()).limit(limit)

    if status:
        query = query.where(Conversation.status == status)
    if agent_id:
        query = query.where(Conversation.agent_id == agent_id)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/conversations/{conversation_id}", response_model=ConversationDetail)
async def get_conversation(
    conversation_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get full conversation with messages and customer info."""
    result = await db.execute(
        select(Conversation)
        .options(selectinload(Conversation.messages), selectinload(Conversation.customer))
        .where(Conversation.id == conversation_id)
    )
    conversation = result.scalar_one_or_none()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.post("/conversations/{conversation_id}/resolve")
async def resolve_conversation(
    conversation_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Mark a conversation as resolved."""
    conversation = await db.get(Conversation, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    conversation.status = ConversationStatus.RESOLVED
    conversation.resolved_at = datetime.utcnow()

    # Free up agent capacity
    if conversation.agent_id:
        agent = await db.get(Agent, conversation.agent_id)
        if agent and agent.active_conversations > 0:
            agent.active_conversations -= 1
            if agent.active_conversations < agent.max_concurrent:
                agent.is_available = True

    return {"status": "resolved", "conversation_id": str(conversation_id)}


@router.get("/customers/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get customer profile."""
    customer = await db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.get("/dashboard/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics(
    db: AsyncSession = Depends(get_db),
):
    """Get real-time dashboard metrics for supervisors."""
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # Active conversations
    active_result = await db.execute(
        select(func.count(Conversation.id)).where(
            Conversation.status.in_([
                ConversationStatus.ACTIVE,
                ConversationStatus.WAITING_AGENT,
                ConversationStatus.WAITING_CUSTOMER,
                ConversationStatus.ESCALATED,
            ])
        )
    )
    active_count = active_result.scalar() or 0

    # In queue (waiting for agent)
    queue_result = await db.execute(
        select(func.count(Conversation.id)).where(
            Conversation.status == ConversationStatus.WAITING_AGENT
        )
    )
    queue_count = queue_result.scalar() or 0

    # AI auto-resolved today
    ai_resolved_result = await db.execute(
        select(func.count(Conversation.id)).where(
            Conversation.ai_auto_resolved == True,
            Conversation.created_at >= today_start,
        )
    )
    ai_resolved = ai_resolved_result.scalar() or 0

    # Total resolved today
    total_resolved_result = await db.execute(
        select(func.count(Conversation.id)).where(
            Conversation.status == ConversationStatus.RESOLVED,
            Conversation.resolved_at >= today_start,
        )
    )
    total_resolved = total_resolved_result.scalar() or 0

    # Agent counts
    agents_online_result = await db.execute(
        select(func.count(Agent.id)).where(Agent.is_online == True)
    )
    agents_online = agents_online_result.scalar() or 0

    agents_available_result = await db.execute(
        select(func.count(Agent.id)).where(Agent.is_available == True)
    )
    agents_available = agents_available_result.scalar() or 0

    ai_pct = (ai_resolved / max(total_resolved, 1)) * 100

    return DashboardMetrics(
        active_conversations=active_count,
        in_queue=queue_count,
        avg_wait_minutes=1.5,  # Would compute from actual queue times
        ai_auto_resolved_today=ai_resolved,
        ai_auto_resolved_pct=round(ai_pct, 1),
        avg_handle_time_minutes=4.2,  # Would compute from actual resolution times
        csat_today=None,
        agents_online=agents_online,
        agents_available=agents_available,
    )
