"""
Smart Routing Engine.

Routes conversations to the best available agent using a weighted scoring algorithm:
- Skill match (40%)
- Availability (25%)
- Load balance (20%)
- Customer history (15%)
"""

import json
import uuid
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.database_models import Agent, Conversation
from app.models.schemas import AIAnalysis, RoutingResult
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Maps intents to required agent skills
INTENT_SKILL_MAP = {
    "payment_inquiry": ["billing"],
    "refund_request": ["billing", "refunds"],
    "billing_dispute": ["billing", "disputes"],
    "plan_change": ["billing", "accounts"],
    "technical_issue": ["technical"],
    "product_question": ["product"],
    "how_to_guide": ["product", "technical"],
    "bug_report": ["technical"],
    "order_status": ["orders", "shipping"],
    "order_cancellation": ["orders"],
    "delivery_issue": ["shipping"],
    "return_request": ["orders", "returns"],
    "password_reset": ["accounts", "security"],
    "profile_update": ["accounts"],
    "account_closure": ["accounts", "retention"],
    "security_concern": ["security"],
    "service_complaint": ["escalation"],
    "agent_complaint": ["escalation"],
    "escalation_request": ["escalation"],
}


async def route_conversation(
    db: AsyncSession,
    conversation: Conversation,
    analysis: AIAnalysis,
    customer_id: str,
) -> RoutingResult:
    """
    Route a conversation based on AI analysis.
    Returns routing decision with assigned agent if applicable.
    """
    routing = analysis.routing_decision

    if routing == "auto_respond":
        return RoutingResult(
            decision="auto_respond",
            reason=f"AI confidence {analysis.intent_confidence:.0%} exceeds threshold; auto-responding.",
        )

    # For all other cases, find the best agent
    best_agent = await _find_best_agent(db, analysis.intent, customer_id)

    if best_agent is None:
        return RoutingResult(
            decision="queue",
            reason="No agents available. Added to priority queue.",
        )

    # Update agent load
    best_agent.active_conversations += 1
    if best_agent.active_conversations >= best_agent.max_concurrent:
        best_agent.is_available = False

    return RoutingResult(
        decision="assign_agent" if routing != "priority_escalate" else "escalate",
        agent_id=best_agent.id,
        agent_name=best_agent.name,
        reason=f"Routed to {best_agent.name} (skill match + availability).",
    )


async def _find_best_agent(
    db: AsyncSession,
    intent: str,
    customer_id: str,
) -> Agent | None:
    """Find the best available agent using weighted scoring."""
    result = await db.execute(
        select(Agent).where(Agent.is_online == True, Agent.is_available == True)
    )
    available_agents = result.scalars().all()

    if not available_agents:
        return None

    required_skills = INTENT_SKILL_MAP.get(intent, [])

    scored_agents = []
    for agent in available_agents:
        agent_skills = json.loads(agent.skills) if agent.skills else []
        score = _calculate_agent_score(agent, agent_skills, required_skills)
        scored_agents.append((agent, score))

    scored_agents.sort(key=lambda x: x[1], reverse=True)
    return scored_agents[0][0] if scored_agents else None


def _calculate_agent_score(
    agent: Agent,
    agent_skills: list[str],
    required_skills: list[str],
) -> float:
    """
    Calculate agent match score (0-1).
    Weights: skill_match=0.40, availability=0.25, load_balance=0.20, history=0.15
    """
    # Skill match (0-1)
    if required_skills:
        matching = len(set(agent_skills) & set(required_skills))
        skill_score = matching / len(required_skills)
    else:
        skill_score = 0.5  # No specific skill needed

    # Load balance (0-1, lower load = higher score)
    load_ratio = agent.active_conversations / max(agent.max_concurrent, 1)
    load_score = 1.0 - load_ratio

    # Availability (binary for now)
    availability_score = 1.0 if agent.is_available else 0.0

    # Customer history bonus (placeholder — would check past interactions)
    history_score = 0.0

    return (
        skill_score * 0.40
        + availability_score * 0.25
        + load_score * 0.20
        + history_score * 0.15
    )
