import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models.database_models import ChannelType, ConversationStatus, MessageSender


# --- Customer Schemas ---

class CustomerCreate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    segment: str = "standard"


class CustomerResponse(BaseModel):
    id: str
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    segment: str
    lifetime_value: float
    csat_avg: Optional[float]
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Message Schemas ---

class InboundMessage(BaseModel):
    """Message coming from any channel adapter."""
    channel: ChannelType
    customer_identifier: str  # phone, email, or session ID depending on channel
    content: str
    content_type: str = "text"
    metadata: dict = Field(default_factory=dict)


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    sender: MessageSender
    channel: ChannelType
    content: str
    content_type: str
    ai_confidence: Optional[float]
    ai_intent: Optional[str]
    ai_sentiment: Optional[float]
    ai_suggested: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Conversation Schemas ---

class ConversationResponse(BaseModel):
    id: str
    customer_id: str
    agent_id: Optional[str]
    channel: ChannelType
    status: ConversationStatus
    intent: Optional[str]
    intent_confidence: Optional[float]
    sentiment_score: Optional[float]
    urgency: int
    ai_auto_resolved: bool
    summary: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ConversationDetail(ConversationResponse):
    customer: CustomerResponse
    messages: list[MessageResponse] = []

    model_config = {"from_attributes": True}


# --- AI Analysis Schemas ---

class AIAnalysis(BaseModel):
    """Result from the AI analysis pipeline."""
    intent: str
    intent_confidence: float
    sentiment_score: float  # -1.0 to 1.0
    sentiment_label: str  # positive, neutral, negative
    urgency: int  # 1-5
    entities: dict = Field(default_factory=dict)
    suggested_response: Optional[str] = None
    suggested_actions: list[str] = Field(default_factory=list)
    routing_decision: str  # auto_respond, suggest_to_agent, escalate, priority_escalate
    confidence_explanation: str = ""


class AIResponseDraft(BaseModel):
    """AI-generated response for agent review or auto-send."""
    response_text: str
    confidence: float
    sources: list[str] = Field(default_factory=list)  # KB articles or past conversations referenced
    actions: list[str] = Field(default_factory=list)
    internal_notes: str = ""


# --- Agent Schemas ---

class AgentCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str = "agent"
    skills: list[str] = Field(default_factory=list)


class AgentResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    skills: str
    max_concurrent: int
    is_online: bool
    is_available: bool
    active_conversations: int

    model_config = {"from_attributes": True}


class AgentLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- Dashboard Schemas ---

class DashboardMetrics(BaseModel):
    active_conversations: int
    in_queue: int
    avg_wait_minutes: float
    ai_auto_resolved_today: int
    ai_auto_resolved_pct: float
    avg_handle_time_minutes: float
    csat_today: Optional[float]
    agents_online: int
    agents_available: int


class RoutingResult(BaseModel):
    decision: str  # auto_respond, assign_agent, escalate
    agent_id: Optional[str] = None
    agent_name: Optional[str] = None
    reason: str = ""
