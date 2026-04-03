import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import (
    Column, String, Float, Integer, DateTime, Text, ForeignKey, Boolean, Enum as SAEnum
)
from sqlalchemy.orm import relationship
from app.db.database import Base


def _uuid_default():
    return str(uuid.uuid4())


class ChannelType(str, Enum):
    WHATSAPP = "whatsapp"
    EMAIL = "email"
    WEBCHAT = "webchat"
    VOICE = "voice"
    SOCIAL_FB = "social_fb"
    SOCIAL_IG = "social_ig"
    SOCIAL_X = "social_x"


class ConversationStatus(str, Enum):
    ACTIVE = "active"
    WAITING_AGENT = "waiting_agent"
    WAITING_CUSTOMER = "waiting_customer"
    RESOLVED = "resolved"
    ESCALATED = "escalated"


class MessageSender(str, Enum):
    CUSTOMER = "customer"
    AGENT = "agent"
    AI = "ai"
    SYSTEM = "system"


class UrgencyLevel(int, Enum):
    MINIMAL = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5


class Customer(Base):
    __tablename__ = "customers"

    id = Column(String(36), primary_key=True, default=_uuid_default)
    external_id = Column(String(255), unique=True, index=True, nullable=True)
    name = Column(String(255), nullable=True)
    email = Column(String(255), index=True, nullable=True)
    phone = Column(String(50), index=True, nullable=True)
    segment = Column(String(50), default="standard")  # standard, premium, enterprise
    metadata_json = Column(Text, default="{}")
    lifetime_value = Column(Float, default=0.0)
    csat_avg = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    conversations = relationship("Conversation", back_populates="customer")


class Agent(Base):
    __tablename__ = "agents"

    id = Column(String(36), primary_key=True, default=_uuid_default)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="agent")  # agent, supervisor, admin
    skills = Column(Text, default="[]")  # JSON array of skill tags
    max_concurrent = Column(Integer, default=8)
    is_online = Column(Boolean, default=False)
    is_available = Column(Boolean, default=False)
    active_conversations = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    assigned_conversations = relationship("Conversation", back_populates="assigned_agent")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String(36), primary_key=True, default=_uuid_default)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False)
    agent_id = Column(String(36), ForeignKey("agents.id"), nullable=True)
    channel = Column(SAEnum(ChannelType), nullable=False)
    status = Column(SAEnum(ConversationStatus), default=ConversationStatus.ACTIVE)
    intent = Column(String(100), nullable=True)
    intent_confidence = Column(Float, nullable=True)
    sentiment_score = Column(Float, nullable=True)  # -1.0 to 1.0
    urgency = Column(Integer, default=2)
    ai_auto_resolved = Column(Boolean, default=False)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    customer = relationship("Customer", back_populates="conversations")
    assigned_agent = relationship("Agent", back_populates="assigned_conversations")
    messages = relationship("Message", back_populates="conversation", order_by="Message.created_at")


class Message(Base):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=_uuid_default)
    conversation_id = Column(String(36), ForeignKey("conversations.id"), nullable=False)
    sender = Column(SAEnum(MessageSender), nullable=False)
    sender_id = Column(String(36), nullable=True)  # agent or customer UUID
    channel = Column(SAEnum(ChannelType), nullable=False)
    content = Column(Text, nullable=False)
    content_type = Column(String(50), default="text")  # text, image, file, audio
    ai_confidence = Column(Float, nullable=True)
    ai_intent = Column(String(100), nullable=True)
    ai_sentiment = Column(Float, nullable=True)
    ai_suggested = Column(Boolean, default=False)  # True if AI-generated suggestion
    metadata_json = Column(Text, default="{}")
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")


class AIDecisionLog(Base):
    __tablename__ = "ai_decision_logs"

    id = Column(String(36), primary_key=True, default=_uuid_default)
    conversation_id = Column(String(36), ForeignKey("conversations.id"), nullable=False)
    message_id = Column(String(36), ForeignKey("messages.id"), nullable=True)
    decision_type = Column(String(50), nullable=False)  # auto_respond, suggest, escalate, route
    intent = Column(String(100), nullable=True)
    confidence = Column(Float, nullable=True)
    sentiment = Column(Float, nullable=True)
    urgency = Column(Integer, nullable=True)
    action_taken = Column(String(100), nullable=False)
    reasoning = Column(Text, nullable=True)
    agent_override = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
