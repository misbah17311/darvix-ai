# Business Case Document
## DARVIX — Financial Justification & Market Analysis

**Version:** 1.0  
**Date:** April 3, 2026  

---

## 1. TAM / SAM / SOM

### Market Sizing

```
┌─────────────────────────────────────────────────────────────────────┐
│                     MARKET OPPORTUNITY                               │
│                                                                      │
│  ┌────────────────────────────────────────────────────────┐         │
│  │                                                        │         │
│  │                    TAM: $29.1B                         │         │
│  │            Global CX + Contact Center                  │         │
│  │              AI Market (2026)                           │         │
│  │                                                        │         │
│  │      ┌────────────────────────────────┐               │         │
│  │      │                                │               │         │
│  │      │         SAM: $8.4B             │               │         │
│  │      │   Omnichannel AI Platforms     │               │         │
│  │      │   (Mid-market + Enterprise)    │               │         │
│  │      │                                │               │         │
│  │      │    ┌──────────────────┐       │               │         │
│  │      │    │                  │       │               │         │
│  │      │    │  SOM: $420M      │       │               │         │
│  │      │    │  5% penetration  │       │               │         │
│  │      │    │  Year 3 target   │       │               │         │
│  │      │    │                  │       │               │         │
│  │      │    └──────────────────┘       │               │         │
│  │      │                                │               │         │
│  │      └────────────────────────────────┘               │         │
│  │                                                        │         │
│  └────────────────────────────────────────────────────────┘         │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Detailed Breakdown

| Metric | Value | Source / Methodology |
|--------|-------|---------------------|
| **TAM (Total Addressable Market)** | $29.1B (2026) | Global contact center AI ($18.2B) + CX platform market ($10.9B). CAGR 23.4%. Sources: Gartner, MarketsandMarkets |
| **SAM (Serviceable Addressable Market)** | $8.4B | Filtered to: omnichannel AI platforms (not point solutions), mid-market ($50M-$1B revenue) + enterprise (>$1B revenue), B2C companies with >1000 daily customer interactions, North America + Europe + APAC tier 1 |
| **SOM (Serviceable Obtainable Market)** | $420M (Year 3) | 5% SAM penetration. Based on: 200-400 enterprise customers at $100K-$2M ARR, competitive positioning vs. Zendesk AI, Salesforce Einstein, Intercom Fin |

### Market Tailwinds

| Trend | Impact on DARVIX |
|-------|-----------------|
| GenAI adoption in enterprise (2024-2027 boom) | Enterprises actively seeking AI CX solutions; buyer education done |
| Channel fragmentation increasing (avg 4.5 channels/customer) | Core problem DARVIX solves — more channels = more pain |
| Labor costs rising (agent salaries +12% YoY) | ROI of AI automation becomes more compelling every year |
| Customer expectation of instant response (78% expect <5 min) | Only AI can meet this at scale; human-only models fail |
| Privacy regulations tightening (GDPR, AI Act) | Safety-first design is competitive advantage in regulated markets |

---

## 2. Cost Savings Analysis

### For a Typical DARVIX Customer (Mid-Market: 50 agents, 150K interactions/month)

#### Current State (Without DARVIX)

| Cost Category | Monthly Cost | Annual Cost |
|--------------|-------------|-------------|
| Agent salaries (50 × $4,500/mo) | $225,000 | $2,700,000 |
| Agent tools & licenses (Zendesk/Intercom) | $12,500 | $150,000 |
| Training & onboarding (15% turnover) | $8,000 | $96,000 |
| Supervision & QA (5 supervisors) | $37,500 | $450,000 |
| Channel-specific tools (WhatsApp Business API, etc.) | $5,000 | $60,000 |
| **Total Current Cost** | **$288,000** | **$3,456,000** |

#### With DARVIX (After 6-month ramp)

| Cost Category | Monthly Cost | Savings | Notes |
|--------------|-------------|---------|-------|
| Agent salaries (35 agents — 30% reduction) | $157,500 | $67,500/mo | AI handles 55% of L1; agents handle more volume |
| DARVIX platform license | $25,000 | — | Replaces multiple tools |
| AI compute costs (OpenAI API) | $3,000 | — | Tiered routing minimizes cost |
| Remaining tools & overhead | $8,000 | $9,500/mo | Consolidated into DARVIX |
| Training (lower turnover with AI assist) | $4,000 | $4,000/mo | Agents more satisfied with AI support |
| Supervision (3 supervisors — AI dashboards) | $22,500 | $15,000/mo | Automated monitoring reduces need |
| **Total With DARVIX** | **$220,000** | **$68,000/mo** | |

#### Annual Savings Summary

| Category | Annual Savings |
|----------|---------------|
| **Direct labor savings** (15 fewer agents) | $810,000 |
| **Tool consolidation** | $114,000 |
| **Reduced training costs** | $48,000 |
| **Supervision efficiency** | $180,000 |
| **Faster resolution → fewer escalations** | $120,000 |
| **Total Annual Savings** | **$1,272,000** |
| **DARVIX Annual Cost** | **($336,000)** |
| **Net Annual Savings** | **$936,000** |

---

## 3. Revenue Potential

### Revenue Streams for DARVIX

| Stream | Model | Year 1 | Year 2 | Year 3 |
|--------|-------|--------|--------|--------|
| **SaaS Subscriptions** | Tiered per agent seat + message volume | $2.4M | $9.6M | $28.8M |
| **AI Usage (Overage)** | Per-message beyond plan limits | $0.3M | $1.8M | $6.2M |
| **Professional Services** | Implementation, training, customization | $0.8M | $2.4M | $4.8M |
| **Channel Adapter Add-ons** | Premium channels (voice, social) | $0.1M | $1.2M | $4.0M |
| **Analytics & Insights** | Advanced reporting module | — | $0.6M | $2.0M |
| **API Marketplace** | Third-party integrations (rev share) | — | $0.2M | $1.2M |
| **Total Revenue** | | **$3.6M** | **$15.8M** | **$47.0M** |

### Pricing Tiers

| Plan | Monthly Price | Includes | Target |
|------|-------------|----------|--------|
| **Starter** | $99/agent + $0.02/msg | 3 channels, basic AI, 5K msgs | SMB (5-20 agents) |
| **Professional** | $199/agent + $0.015/msg | All channels, full AI, 50K msgs | Mid-market (20-100 agents) |
| **Enterprise** | Custom ($300+/agent) | Unlimited, custom AI, SLA, dedicated support | Enterprise (100+ agents) |

### Revenue Impact for DARVIX Customers

DARVIX doesn't just save costs — it generates revenue:

| Revenue Driver | Mechanism | Estimated Impact |
|---------------|-----------|-----------------|
| **Reduced churn** | Better CX → higher retention | 3-5% churn reduction → $500K-$2M/yr for mid-market |
| **Upsell/cross-sell** | Next Best Action engine suggests offers in context | 8-12% increase in conversion on AI-suggested offers |
| **Higher CSAT → NPS → referrals** | Every 1-point NPS increase = 2% revenue growth | Measurable through attribution tracking |
| **Faster resolution → more capacity** | Same team handles 2x volume | Supports business growth without linear headcount |

---

## 4. ROI Calculation

### Customer ROI (Mid-Market Example: 50 agents)

```
┌─────────────────────────────────────────────────────────────────┐
│                   3-YEAR ROI CALCULATION                         │
│                   (Typical Mid-Market Customer)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  INVESTMENT                                                      │
│  ──────────                                                      │
│  Year 0: Implementation + setup              $50,000            │
│  Year 1: DARVIX license ($25K/mo × 12)       $300,000           │
│  Year 2: DARVIX license (growth: 60 agents)  $360,000           │
│  Year 3: DARVIX license (growth: 70 agents)  $420,000           │
│  ────────────────────────────────────────────────────            │
│  Total 3-Year Investment:                    $1,130,000          │
│                                                                  │
│  RETURNS                                                         │
│  ───────                                                         │
│  Year 1: Cost savings (ramping)              $624,000            │
│  Year 1: Revenue uplift (churn + upsell)     $400,000            │
│  Year 2: Cost savings (full)                 $1,272,000          │
│  Year 2: Revenue uplift                      $800,000            │
│  Year 3: Cost savings (optimized)            $1,500,000          │
│  Year 3: Revenue uplift                      $1,200,000          │
│  ────────────────────────────────────────────────────            │
│  Total 3-Year Returns:                       $5,796,000          │
│                                                                  │
│  ═══════════════════════════════════════════════════════         │
│                                                                  │
│  NET BENEFIT (3-Year):          $4,666,000                      │
│  ROI:                           413%                             │
│  PAYBACK PERIOD:                5.4 months                       │
│                                                                  │
│  ═══════════════════════════════════════════════════════         │
└─────────────────────────────────────────────────────────────────┘
```

### DARVIX Company ROI (For Investors)

| Metric | Year 1 | Year 2 | Year 3 |
|--------|--------|--------|--------|
| **Revenue** | $3.6M | $15.8M | $47.0M |
| **COGS** (infra + AI compute) | $1.1M | $3.8M | $9.4M |
| **Gross Margin** | 69% | 76% | 80% |
| **OpEx** (team + G&A + S&M) | $4.8M | $10.2M | $18.0M |
| **EBITDA** | -$2.3M | $1.8M | $19.6M |
| **Customers** | 30 | 120 | 350 |
| **ARR** | $3.6M | $15.8M | $47.0M |
| **Net Revenue Retention** | — | 135% | 140% |

### Competitive Positioning

| Competitor | Strengths | DARVIX Advantage |
|-----------|-----------|-----------------|
| **Zendesk AI** | Massive install base, brand recognition | True omnichannel unification (Zendesk bolted on AI to ticketing) |
| **Salesforce Einstein** | CRM integration, enterprise trust | AI-native architecture vs. AI added to existing CRM; 10x faster deploy |
| **Intercom Fin** | Best-in-class chat AI | Single-channel focus; DARVIX covers voice, email, social too |
| **Freshdesk Freddy** | Price-competitive, SMB friendly | Superior AI accuracy (RAG + multi-model); better cross-channel |
| **Custom builds** | Full control | 6-month head start; continuously improving; lower TCO than in-house |

### Risk Analysis

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| LLM cost increases | Medium | High | Multi-model strategy; can swap providers; tiered routing minimizes usage |
| Enterprise sales cycle >6 months | High | Medium | Land with mid-market; expand into enterprise; product-led growth for SMB |
| AI accuracy issues erode trust | Medium | Critical | Safety-first architecture; human-in-the-loop; confidence gating |
| Competitor with similar offering | High | Medium | Speed of execution; vertical specialization; superior UX |
| Regulatory changes (AI Act, etc.) | Medium | Medium | Compliance built into architecture; transparency by design |

---

## 5. Executive Summary

> **DARVIX is an AI-powered omnichannel customer experience platform that unifies support across WhatsApp, email, voice, web chat, and social into a single intelligent system.**
>
> **The market:** $29.1B TAM growing at 23.4% CAGR, driven by AI adoption and channel fragmentation.
>
> **The value:** Customers save $936K/year (mid-market) with 413% 3-year ROI and 5.4-month payback.
>
> **The business:** $47M ARR by Year 3, 80% gross margins, with a clear path to profitability in Year 2.
>
> **The moat:** AI-native architecture (not bolted-on AI), true cross-channel intelligence, and safety-first design that earns enterprise trust.
