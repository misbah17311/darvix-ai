"""
Agent authentication & management API routes.
"""

import uuid
import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.database_models import Agent
from app.models.schemas import AgentCreate, AgentResponse, AgentLogin, TokenResponse
from app.core.auth import hash_password, verify_password, create_access_token, get_current_agent

router = APIRouter(prefix="/api/agents", tags=["agents"])


@router.post("/register", response_model=AgentResponse, status_code=201)
async def register_agent(
    agent_data: AgentCreate,
    db: AsyncSession = Depends(get_db),
):
    """Register a new agent."""
    # Check if email already exists
    existing = await db.execute(select(Agent).where(Agent.email == agent_data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    agent = Agent(
        id=str(uuid.uuid4()),
        name=agent_data.name,
        email=agent_data.email,
        password_hash=hash_password(agent_data.password),
        role=agent_data.role,
        skills=json.dumps(agent_data.skills),
    )
    db.add(agent)
    await db.flush()
    return agent


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: AgentLogin,
    db: AsyncSession = Depends(get_db),
):
    """Authenticate an agent and return JWT token."""
    result = await db.execute(select(Agent).where(Agent.email == credentials.email))
    agent = result.scalar_one_or_none()

    if not agent or not verify_password(credentials.password, agent.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token({
        "sub": str(agent.id),
        "email": agent.email,
        "role": agent.role,
    })

    # Mark agent as online
    agent.is_online = True
    agent.is_available = True

    return TokenResponse(access_token=token)


@router.post("/logout")
async def logout(
    current_agent: dict = Depends(get_current_agent),
    db: AsyncSession = Depends(get_db),
):
    """Mark agent as offline."""
    agent = await db.get(Agent, current_agent["sub"])
    if agent:
        agent.is_online = False
        agent.is_available = False
    return {"status": "logged out"}


@router.get("/me", response_model=AgentResponse)
async def get_current_agent_profile(
    current_agent: dict = Depends(get_current_agent),
    db: AsyncSession = Depends(get_db),
):
    """Get current agent's profile."""
    agent = await db.get(Agent, current_agent["sub"])
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.get("/", response_model=list[AgentResponse])
async def list_agents(
    online_only: bool = False,
    db: AsyncSession = Depends(get_db),
):
    """List all agents."""
    query = select(Agent)
    if online_only:
        query = query.where(Agent.is_online == True)
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/{agent_id}/status")
async def update_agent_status(
    agent_id: str,
    body: dict,
    db: AsyncSession = Depends(get_db),
):
    """Update agent online/availability status."""
    agent = await db.get(Agent, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    if "is_available" in body:
        agent.is_available = body["is_available"]
    if "is_online" in body:
        agent.is_online = body["is_online"]

    return {"status": "updated"}
