# AI Blueprint
## DARVIX — AI Architecture & Model Design

**Version:** 1.0  
**Date:** April 3, 2026  

---

## 1. Data Flow Diagram

### End-to-End Data Flow

```
                            DARVIX AI PLATFORM — DATA FLOW
                            ═══════════════════════════════

 ┌──────────────────────────── INGESTION LAYER ──────────────────────────────┐
 │                                                                            │
 │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
 │  │ WhatsApp │ │  Email   │ │  Voice   │ │ Web Chat │ │  Social  │       │
 │  │ Adapter  │ │ Adapter  │ │ Adapter  │ │ Adapter  │ │ Adapter  │       │
 │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘       │
 │       │             │            │             │             │              │
 │       └─────────────┴──────┬─────┴─────────────┴─────────────┘              │
 │                            ▼                                                │
 │              ┌─────────────────────────┐                                    │
 │              │  NORMALIZED MESSAGE     │  { customer_id, channel,           │
 │              │  SCHEMA                 │    content, timestamp,             │
 │              │                         │    metadata, attachments }         │
 │              └────────────┬────────────┘                                    │
 └───────────────────────────┼────────────────────────────────────────────────┘
                             ▼
 ┌──────────────────── MESSAGE BUS (Redis Streams) ───────────────────────────┐
 │                                                                             │
 │   Stream: messages.inbound    →    Consumer Groups per AI service           │
 │   Stream: messages.outbound   ←    Processed responses                     │
 │   Stream: events.actions      →    Action execution pipeline               │
 │   Stream: events.analytics    →    Analytics & logging pipeline             │
 │                                                                             │
 └───────────────────────────┬─────────────────────────────────────────────────┘
                             ▼
 ┌──────────────────── AI PROCESSING PIPELINE ────────────────────────────────┐
 │                                                                             │
 │   STEP 1: IDENTITY RESOLUTION                                              │
 │   ┌────────────────────────────────────┐                                   │
 │   │ • Match customer across channels    │  ← PostgreSQL (customer profiles) │
 │   │ • Merge conversation threads        │  ← Fuzzy match: email+phone+name │
 │   │ • Load customer context & history   │  ← ChromaDB (embeddings)         │
 │   └──────────────┬─────────────────────┘                                   │
 │                  ▼                                                          │
 │   STEP 2: AI ANALYSIS (Parallel Execution)                                 │
 │   ┌─────────────────┐ ┌─────────────────┐ ┌──────────────────┐            │
 │   │ INTENT          │ │ SENTIMENT       │ │ URGENCY          │            │
 │   │ CLASSIFICATION  │ │ ANALYSIS        │ │ PREDICTION       │            │
 │   │                 │ │                 │ │                  │            │
 │   │ Model: LLM     │ │ Model: LLM +   │ │ Model: LLM +    │            │
 │   │ (GPT-4o-mini)  │ │ fine-tuned      │ │ rule engine     │            │
 │   │                 │ │ classifier      │ │                  │            │
 │   │ Output:        │ │ Output:         │ │ Output:          │            │
 │   │ - intent_label │ │ - score (-1→+1) │ │ - urgency (1-5)  │            │
 │   │ - confidence   │ │ - emotion tags  │ │ - sla_deadline   │            │
 │   │ - entities     │ │ - trend         │ │ - escalate_flag  │            │
 │   └───────┬────────┘ └───────┬─────────┘ └────────┬─────────┘            │
 │           └───────────────────┼──────────────────────┘                      │
 │                               ▼                                             │
 │   STEP 3: CONTEXT ENRICHMENT                                               │
 │   ┌────────────────────────────────────┐                                   │
 │   │ • Retrieve relevant past           │  ← ChromaDB (semantic search)     │
 │   │   conversations (RAG)              │                                   │
 │   │ • Load customer profile data       │  ← PostgreSQL                     │
 │   │ • Fetch knowledge base articles    │  ← ChromaDB (KB embeddings)       │
 │   │ • Check active policies/offers     │  ← Business rules engine          │
 │   └──────────────┬─────────────────────┘                                   │
 │                  ▼                                                          │
 │   STEP 4: DECISION ENGINE                                                  │
 │   ┌────────────────────────────────────┐                                   │
 │   │              ROUTER                │                                   │
 │   │                                    │                                   │
 │   │  Confidence ≥ 0.85 AND             │                                   │
 │   │  Risk = LOW                        │──→ AUTO-RESPOND (AI handles)      │
 │   │                                    │                                   │
 │   │  Confidence ≥ 0.70 AND             │                                   │
 │   │  Risk = MEDIUM                     │──→ SUGGEST TO AGENT               │
 │   │                                    │    (AI drafts, human approves)    │
 │   │                                    │                                   │
 │   │  Confidence < 0.70 OR              │                                   │
 │   │  Risk = HIGH                       │──→ ESCALATE TO AGENT              │
 │   │                                    │    (Full context handoff)         │
 │   │                                    │                                   │
 │   │  Urgency = 5 (Critical)           │──→ PRIORITY ESCALATION            │
 │   │                                    │    (Alert supervisor + top agent) │
 │   └──────────────┬─────────────────────┘                                   │
 │                  ▼                                                          │
 │   STEP 5: RESPONSE GENERATION                                              │
 │   ┌────────────────────────────────────┐                                   │
 │   │ LLM (GPT-4o) with:                │                                   │
 │   │ • System prompt (brand voice)      │                                   │
 │   │ • Customer context (RAG results)   │                                   │
 │   │ • Conversation history             │                                   │
 │   │ • Action instructions              │                                   │
 │   │                                    │                                   │
 │   │ Output:                            │                                   │
 │   │ • response_text                    │                                   │
 │   │ • suggested_actions[]              │                                   │
 │   │ • internal_notes                   │                                   │
 │   └──────────────┬─────────────────────┘                                   │
 │                  ▼                                                          │
 │   STEP 6: SAFETY FILTER                                                    │
 │   ┌────────────────────────────────────┐                                   │
 │   │ • PII redaction (outbound)         │                                   │
 │   │ • Toxicity check                   │                                   │
 │   │ • Hallucination guardrail          │                                   │
 │   │ • Policy compliance check          │                                   │
 │   └────────────────────────────────────┘                                   │
 │                                                                             │
 └─────────────────────────────────────────────────────────────────────────────┘
                             ▼
 ┌──────────────────── OUTPUT / ACTION LAYER ──────────────────────────────────┐
 │                                                                              │
 │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
 │   │ Send Reply   │  │  Execute     │  │  Create      │  │  Update      │  │
 │   │ (via channel │  │  Action      │  │  Ticket      │  │  CRM         │  │
 │   │  adapter)    │  │  (refund,    │  │  (Jira/      │  │  (Salesforce │  │
 │   │              │  │   cancel)    │  │   internal)  │  │   /HubSpot)  │  │
 │   └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  │
 │                                                                              │
 └──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. AI Model Usage

### Model Architecture Overview

| Component | Model / Approach | Why This Choice | Latency Target |
|-----------|-----------------|----------------|----------------|
| **Intent Classification** | GPT-4o-mini with structured output | High accuracy on diverse intents; no training data needed for MVP | < 500ms |
| **Sentiment Analysis** | GPT-4o-mini + distilled classifier | LLM for nuanced sentiment; lightweight model for high-volume scoring | < 300ms |
| **Urgency Prediction** | LLM reasoning + rule-based boost | Rules handle known urgent keywords; LLM handles contextual urgency | < 500ms |
| **Response Generation** | GPT-4o with RAG context | Best quality for customer-facing text; RAG grounds in company data | < 2s |
| **Entity Extraction** | GPT-4o-mini structured output | Extract order IDs, dates, product names, account numbers | < 400ms |
| **Conversation Embedding** | text-embedding-3-small (OpenAI) | Low cost, high quality for semantic search in ChromaDB | < 200ms |
| **Knowledge Base Search** | ChromaDB + embedding similarity | Retrieve relevant KB articles/past resolutions for RAG context | < 100ms |
| **Identity Resolution** | Fuzzy matching + deterministic rules | Phone/email exact match first; fuzzy on name+metadata second | < 50ms |

### Intent Taxonomy (MVP)

```
ROOT
├── BILLING
│   ├── payment_inquiry
│   ├── refund_request
│   ├── billing_dispute
│   └── plan_change
├── SUPPORT
│   ├── technical_issue
│   ├── product_question
│   ├── how_to_guide
│   └── bug_report
├── ORDER
│   ├── order_status
│   ├── order_cancellation
│   ├── delivery_issue
│   └── return_request
├── ACCOUNT
│   ├── password_reset
│   ├── profile_update
│   ├── account_closure
│   └── security_concern
├── SALES
│   ├── pricing_inquiry
│   ├── upgrade_interest
│   └── new_purchase
├── COMPLAINT
│   ├── service_complaint
│   ├── agent_complaint
│   └── escalation_request
└── OTHER
    ├── general_inquiry
    ├── feedback
    └── unclassified
```

### RAG Pipeline Detail

```
Customer Message
       │
       ▼
┌─────────────────────┐
│ Generate Embedding   │  → text-embedding-3-small
│ of current message   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐     ┌──────────────────────────┐
│ Semantic Search      │────→│ ChromaDB Collections:     │
│ (Top-K = 5)         │     │  • past_conversations     │
│                     │     │  • knowledge_base          │
│                     │     │  • product_catalog          │
│                     │     │  • policy_documents         │
└──────────┬──────────┘     └──────────────────────────┘
           │
           ▼
┌─────────────────────┐
│ Context Assembly     │
│                     │
│ • Customer profile   │  ← PostgreSQL
│ • Conversation hx    │  ← PostgreSQL
│ • RAG results (5)    │  ← ChromaDB
│ • Active offers      │  ← Business rules
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ LLM Prompt Build     │
│                     │
│ System: Brand voice  │
│ + safety rules       │
│ + response format    │
│                     │
│ Context: [assembled] │
│                     │
│ User: [message]      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ GPT-4o Generation    │
│                     │
│ → response_text      │
│ → actions[]          │
│ → confidence_score   │
└─────────────────────┘
```

### LLM Routing Engine

Not all messages need GPT-4o. We use a **tiered routing strategy** to optimize cost and latency:

```
Inbound Message
       │
       ▼
┌─────────────────────────┐
│  COMPLEXITY CLASSIFIER   │  (GPT-4o-mini, ~$0.00015/msg)
│  (lightweight LLM call)  │
└───────────┬─────────────┘
            │
     ┌──────┼──────────┐
     ▼      ▼          ▼
   SIMPLE  MEDIUM    COMPLEX
     │      │          │
     ▼      ▼          ▼
  Cached   GPT-4o    GPT-4o
  Response  -mini    (full)
  or Rule   ($0.0003  ($0.005
  Engine    /msg)     /msg)
```

**Estimated cost at 100K messages/month:**
- 50% Simple (cached/rules): ~$0
- 35% Medium (GPT-4o-mini): ~$10.50
- 15% Complex (GPT-4o): ~$75.00
- Embeddings: ~$5.00
- **Total: ~$90/month** for 100K messages

---

## 3. Safety + Accuracy Plan

### Safety Architecture

```
                    SAFETY LAYERS
                    ═════════════

Layer 1: INPUT VALIDATION
┌─────────────────────────────────────┐
│ • Rate limiting per customer/channel │
│ • Input length limits (4K chars)     │
│ • Injection detection (prompt inject) │
│ • Malicious content filtering        │
└──────────────────┬──────────────────┘
                   ▼
Layer 2: PII PROTECTION
┌─────────────────────────────────────┐
│ • Detect PII (SSN, CC#, etc.)       │
│ • Redact before LLM processing      │
│ • Store PII separately (encrypted)  │
│ • Never include PII in LLM context  │
│ • Regex + NER model for detection    │
└──────────────────┬──────────────────┘
                   ▼
Layer 3: AI GUARDRAILS
┌─────────────────────────────────────┐
│ • Confidence threshold gating        │
│   - ≥0.85: auto-respond             │
│   - 0.70-0.84: suggest to agent     │
│   - <0.70: escalate to human        │
│ • Topic boundary enforcement         │
│   - AI only answers within scope     │
│   - Off-topic → polite redirect      │
│ • Hallucination detection            │
│   - Cross-reference with KB          │
│   - Flag claims not in source docs   │
└──────────────────┬──────────────────┘
                   ▼
Layer 4: OUTPUT VALIDATION
┌─────────────────────────────────────┐
│ • Toxicity scoring (reject > 0.3)   │
│ • Brand voice compliance check      │
│ • PII leak detection (outbound)      │
│ • Response length guardrails         │
│ • No promises AI can't fulfill      │
└──────────────────┬──────────────────┘
                   ▼
Layer 5: HUMAN OVERSIGHT
┌─────────────────────────────────────┐
│ • Agent can override any AI decision │
│ • Supervisor review queue for flags  │
│ • Weekly accuracy audit (sample 5%)  │
│ • Customer feedback loop → retraining│
│ • AI decision audit log (immutable)  │
└─────────────────────────────────────┘
```

### Accuracy Plan

| Strategy | Implementation | Target |
|----------|---------------|--------|
| **Grounded Responses (RAG)** | All AI responses must cite source from KB or customer data | 95% grounding rate |
| **Confidence Calibration** | Weekly calibration of confidence thresholds based on agent override data | < 5% false positive auto-responses |
| **Feedback Loop** | Agent corrections feed back into prompt tuning and few-shot examples | Continuous improvement |
| **A/B Testing** | Shadow mode — AI generates response but agent always reviews for first 2 weeks | Baseline accuracy measurement |
| **Intent Accuracy** | Measure precision/recall per intent category; retrain underperformers | > 90% F1 per category |
| **Sentiment Accuracy** | Validate against agent-labeled samples weekly | > 88% agreement |
| **Drift Detection** | Monitor intent distribution weekly; alert on >10% shift | Auto-alert |

### Incident Response Plan

| Severity | Trigger | Response | Timeline |
|----------|---------|----------|----------|
| **P0 — Critical** | AI sends harmful/incorrect response to customer | Kill switch → all AI to "suggest mode" only | < 5 min |
| **P1 — High** | Accuracy drops below 80% on any category | Disable auto-respond for affected category | < 30 min |
| **P2 — Medium** | Customer reports incorrect AI response | Log + review + update KB/prompts | < 4 hours |
| **P3 — Low** | Drift detected in intent distribution | Investigate + adjust prompts/thresholds | < 24 hours |

### Data Privacy & Compliance

| Requirement | Implementation |
|-------------|---------------|
| **GDPR Right to Erasure** | Customer data deletion API; cascades to all stores including vector embeddings |
| **Data Minimization** | Only store data needed for service; auto-purge after retention period |
| **Consent Management** | Channel-specific consent tracking; opt-out propagates across channels |
| **Encryption** | AES-256 at rest; TLS 1.3 in transit; separate encryption keys per tenant |
| **Access Control** | RBAC with principle of least privilege; MFA for all admin access |
| **Audit Trail** | Immutable log of all AI decisions, data access, and agent actions |
| **Model Transparency** | Explain AI decisions to customers on request (confidence + source cited) |
