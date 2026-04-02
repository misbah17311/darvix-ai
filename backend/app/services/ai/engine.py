"""
AI Engine — Core analysis pipeline for DARVIX.

Processes inbound messages through:
1. Intent Classification
2. Sentiment Analysis
3. Urgency Prediction
4. Response Generation (via RAG)
5. Routing Decision
"""

import json
import logging
from openai import AsyncOpenAI
from app.config import get_settings
from app.models.schemas import AIAnalysis, AIResponseDraft

logger = logging.getLogger(__name__)
settings = get_settings()

client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

INTENT_TAXONOMY = [
    "payment_inquiry", "refund_request", "billing_dispute", "plan_change",
    "technical_issue", "product_question", "how_to_guide", "bug_report",
    "order_status", "order_cancellation", "delivery_issue", "return_request",
    "password_reset", "profile_update", "account_closure", "security_concern",
    "pricing_inquiry", "upgrade_interest", "new_purchase",
    "service_complaint", "agent_complaint", "escalation_request",
    "general_inquiry", "feedback", "unclassified",
]


async def analyze_message(
    message_content: str,
    customer_context: dict | None = None,
    conversation_history: list[dict] | None = None,
) -> AIAnalysis:
    """
    Run the full AI analysis pipeline on an inbound message.
    Returns intent, sentiment, urgency, and routing decision.
    """
    if not client:
        return _fallback_analysis(message_content)

    context_str = ""
    if customer_context:
        context_str = f"\nCustomer context: {json.dumps(customer_context)}"

    history_str = ""
    if conversation_history:
        recent = conversation_history[-10:]  # last 10 messages
        history_str = "\nConversation history:\n" + "\n".join(
            f"  {m.get('sender', '?')}: {m.get('content', '')}" for m in recent
        )

    analysis_prompt = f"""Analyze this customer support message and return a JSON object.

Message: "{message_content}"
{context_str}
{history_str}

Return JSON with these exact fields:
{{
  "intent": "<one of: {', '.join(INTENT_TAXONOMY)}>",
  "intent_confidence": <0.0-1.0>,
  "sentiment_score": <-1.0 to 1.0 where -1=very negative, 0=neutral, 1=very positive>,
  "sentiment_label": "<positive|neutral|negative>",
  "urgency": <1-5 where 1=minimal, 5=critical>,
  "entities": {{"order_id": "...", "product": "...", etc. if found}},
  "confidence_explanation": "<brief reason for the confidence score>"
}}

Rules for urgency scoring:
- 5 (Critical): Service outage, security breach, legal threat, time-critical deadline
- 4 (High): Money lost, delivery failure, account locked, strong negative emotion
- 3 (Medium): Standard support request with some frustration
- 2 (Low): General inquiry, routine question
- 1 (Minimal): Feedback, casual question, follow-up thanks"""

    try:
        response = await client.chat.completions.create(
            model=settings.openai_model_light,
            messages=[
                {"role": "system", "content": "You are an expert customer service AI analyst. Return only valid JSON."},
                {"role": "user", "content": analysis_prompt},
            ],
            temperature=0.1,
            response_format={"type": "json_object"},
        )

        result = json.loads(response.choices[0].message.content)

        # Determine routing decision based on confidence and urgency
        routing = _determine_routing(
            confidence=result.get("intent_confidence", 0),
            urgency=result.get("urgency", 3),
            sentiment=result.get("sentiment_score", 0),
        )

        return AIAnalysis(
            intent=result.get("intent", "unclassified"),
            intent_confidence=result.get("intent_confidence", 0.0),
            sentiment_score=result.get("sentiment_score", 0.0),
            sentiment_label=result.get("sentiment_label", "neutral"),
            urgency=result.get("urgency", 3),
            entities=result.get("entities", {}),
            routing_decision=routing,
            confidence_explanation=result.get("confidence_explanation", ""),
        )

    except Exception as e:
        logger.error(f"AI analysis failed: {e}")
        return _fallback_analysis(message_content)


async def generate_response(
    message_content: str,
    analysis: AIAnalysis,
    customer_context: dict | None = None,
    conversation_history: list[dict] | None = None,
    knowledge_base_results: list[str] | None = None,
) -> AIResponseDraft:
    """
    Generate an AI response using RAG context.
    """
    if not client:
        return AIResponseDraft(
            response_text="Thank you for reaching out. An agent will be with you shortly.",
            confidence=0.5,
        )

    kb_context = ""
    if knowledge_base_results:
        kb_context = "\n\nRelevant knowledge base articles:\n" + "\n---\n".join(knowledge_base_results[:3])

    history_str = ""
    if conversation_history:
        recent = conversation_history[-6:]
        history_str = "\nRecent conversation:\n" + "\n".join(
            f"  {m.get('sender', '?')}: {m.get('content', '')}" for m in recent
        )

    response_prompt = f"""Generate a customer support response.

Customer message: "{message_content}"
Detected intent: {analysis.intent} (confidence: {analysis.intent_confidence})
Customer sentiment: {analysis.sentiment_label} ({analysis.sentiment_score})
Urgency level: {analysis.urgency}/5
{kb_context}
{history_str}

Instructions:
- Be helpful, empathetic, and professional
- If you have specific information (order status, KB article), provide it
- If you need to escalate, acknowledge the issue and explain next steps
- Keep response concise (2-4 sentences for simple queries)
- Match urgency — critical issues get immediate, action-oriented responses
- Never make promises you can't verify
- Never disclose internal system details

Return JSON:
{{
  "response_text": "<the response to send to the customer>",
  "confidence": <0.0-1.0 how confident you are this response is correct>,
  "sources": ["<list of KB articles or data sources used>"],
  "actions": ["<list of suggested actions: create_ticket, issue_refund, escalate, etc.>"],
  "internal_notes": "<notes for the agent about this response>"
}}"""

    try:
        response = await client.chat.completions.create(
            model=settings.openai_model_heavy,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are DARVIX, an AI customer support assistant. "
                        "You are friendly, professional, and efficient. "
                        "Return only valid JSON."
                    ),
                },
                {"role": "user", "content": response_prompt},
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        result = json.loads(response.choices[0].message.content)

        return AIResponseDraft(
            response_text=result.get("response_text", ""),
            confidence=result.get("confidence", 0.5),
            sources=result.get("sources", []),
            actions=result.get("actions", []),
            internal_notes=result.get("internal_notes", ""),
        )

    except Exception as e:
        logger.error(f"AI response generation failed: {e}")
        return AIResponseDraft(
            response_text="Thank you for reaching out. Let me connect you with a specialist who can help.",
            confidence=0.3,
        )


def _determine_routing(confidence: float, urgency: int, sentiment: float) -> str:
    """Determine routing based on AI analysis results."""
    if urgency >= settings.ai_urgency_escalation_threshold:
        return "priority_escalate"
    if confidence >= settings.ai_auto_respond_confidence and urgency <= 2:
        return "auto_respond"
    if confidence >= settings.ai_suggest_confidence:
        return "suggest_to_agent"
    return "escalate"


def _fallback_analysis(message_content: str) -> AIAnalysis:
    """Fallback when AI is unavailable — conservative routing to human."""
    return AIAnalysis(
        intent="unclassified",
        intent_confidence=0.0,
        sentiment_score=0.0,
        sentiment_label="neutral",
        urgency=3,
        routing_decision="escalate",
        confidence_explanation="AI service unavailable; routing to human agent.",
    )
