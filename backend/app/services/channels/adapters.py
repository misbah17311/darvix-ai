"""
Channel Adapter Base + Implementations.

Each channel adapter normalizes inbound messages into a unified schema
and formats outbound messages for the specific channel.
"""

import logging
from abc import ABC, abstractmethod
from app.models.schemas import InboundMessage
from app.models.database_models import ChannelType

logger = logging.getLogger(__name__)


class ChannelAdapter(ABC):
    """Base class for all channel adapters."""

    @abstractmethod
    def channel_type(self) -> ChannelType:
        pass

    @abstractmethod
    async def parse_inbound(self, raw_payload: dict) -> InboundMessage:
        """Parse raw webhook/API payload into normalized InboundMessage."""
        pass

    @abstractmethod
    async def send_outbound(self, recipient: str, message: str, metadata: dict | None = None) -> bool:
        """Send a message to the customer via this channel."""
        pass


class WhatsAppAdapter(ChannelAdapter):
    """WhatsApp Business API adapter."""

    def channel_type(self) -> ChannelType:
        return ChannelType.WHATSAPP

    async def parse_inbound(self, raw_payload: dict) -> InboundMessage:
        # WhatsApp Cloud API webhook format
        entry = raw_payload.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [{}])
        msg = messages[0] if messages else {}

        return InboundMessage(
            channel=ChannelType.WHATSAPP,
            customer_identifier=msg.get("from", ""),
            content=msg.get("text", {}).get("body", ""),
            content_type=msg.get("type", "text"),
            metadata={
                "whatsapp_msg_id": msg.get("id"),
                "timestamp": msg.get("timestamp"),
                "profile_name": value.get("contacts", [{}])[0].get("profile", {}).get("name"),
            },
        )

    async def send_outbound(self, recipient: str, message: str, metadata: dict | None = None) -> bool:
        # In production: call WhatsApp Cloud API
        logger.info(f"[WhatsApp] → {recipient}: {message[:100]}...")
        return True


class EmailAdapter(ChannelAdapter):
    """Email adapter (webhook from SendGrid/Mailgun/etc.)."""

    def channel_type(self) -> ChannelType:
        return ChannelType.EMAIL

    async def parse_inbound(self, raw_payload: dict) -> InboundMessage:
        return InboundMessage(
            channel=ChannelType.EMAIL,
            customer_identifier=raw_payload.get("from_email", ""),
            content=raw_payload.get("text_body", raw_payload.get("html_body", "")),
            content_type="text",
            metadata={
                "subject": raw_payload.get("subject"),
                "message_id": raw_payload.get("message_id"),
                "cc": raw_payload.get("cc", []),
            },
        )

    async def send_outbound(self, recipient: str, message: str, metadata: dict | None = None) -> bool:
        logger.info(f"[Email] → {recipient}: {message[:100]}...")
        return True


class WebChatAdapter(ChannelAdapter):
    """Web chat widget adapter (WebSocket-based)."""

    def channel_type(self) -> ChannelType:
        return ChannelType.WEBCHAT

    async def parse_inbound(self, raw_payload: dict) -> InboundMessage:
        return InboundMessage(
            channel=ChannelType.WEBCHAT,
            customer_identifier=raw_payload.get("session_id", raw_payload.get("email", "")),
            content=raw_payload.get("message", ""),
            content_type=raw_payload.get("type", "text"),
            metadata={
                "session_id": raw_payload.get("session_id"),
                "page_url": raw_payload.get("page_url"),
                "user_agent": raw_payload.get("user_agent"),
            },
        )

    async def send_outbound(self, recipient: str, message: str, metadata: dict | None = None) -> bool:
        # In production: send via WebSocket connection
        logger.info(f"[WebChat] → {recipient}: {message[:100]}...")
        return True


# Channel adapter registry
ADAPTERS: dict[ChannelType, ChannelAdapter] = {
    ChannelType.WHATSAPP: WhatsAppAdapter(),
    ChannelType.EMAIL: EmailAdapter(),
    ChannelType.WEBCHAT: WebChatAdapter(),
}


def get_adapter(channel: ChannelType) -> ChannelAdapter:
    adapter = ADAPTERS.get(channel)
    if not adapter:
        raise ValueError(f"No adapter registered for channel: {channel}")
    return adapter
