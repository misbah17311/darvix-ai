# Wireframes & Journey Maps
## DARVIX — User Experience Design

**Version:** 1.0  
**Date:** April 3, 2026  

---

## 1. Unified Conversation Timeline

### Customer Cross-Channel Journey

```
═══════════════════════════════════════════════════════════════════════════
                    CUSTOMER: Sarah Johnson (#CUS-4821)
                    UNIFIED CONVERSATION TIMELINE
═══════════════════════════════════════════════════════════════════════════

 DAY 1 — March 30, 2026
 ───────────────────────

 09:14 AM  📱 WhatsApp                          INTENT: order_status
 ┌─────────────────────────────────────────────────────────────────────┐
 │ Sarah: "Hi, I ordered a laptop 5 days ago, order #ORD-7392.       │
 │         When will it arrive?"                                       │
 │                                                                     │
 │ 🤖 AI (Auto): "Hi Sarah! I found your order #ORD-7392.            │
 │   Your Dell XPS 15 shipped on March 28 and is currently            │
 │   in transit. Expected delivery: April 1-2.                         │
 │   Tracking: DHL #DHL928374651"                                      │
 │                                                                     │
 │ Sarah: "Thanks!"                                                    │
 │                                                                     │
 │ ✅ RESOLVED by AI | Confidence: 0.94 | Time: 8 seconds             │
 └─────────────────────────────────────────────────────────────────────┘

 DAY 3 — April 1, 2026
 ──────────────────────

 14:22 PM  📧 Email                             INTENT: delivery_issue
 ┌─────────────────────────────────────────────────────────────────────┐
 │ Sarah: "My laptop was supposed to arrive today but tracking        │
 │         says 'delivery exception'. This is urgent - I need it      │
 │         for a presentation tomorrow!"                               │
 │                                                                     │
 │ 🧠 AI Analysis:                                                    │
 │   Intent: delivery_issue (0.96)                                     │
 │   Sentiment: Negative (-0.7) — frustrated, anxious                 │
 │   Urgency: 4/5 (time-sensitive + negative sentiment)               │
 │                                                                     │
 │ ⚡ ROUTED to Agent (confidence for action < threshold)              │
 │   → Agent: Marcus (Shipping Specialist, Load: 3/8)                 │
 │   → AI Suggestion: "Contact DHL for exception details.             │
 │     If unresolvable, offer express re-ship or store pickup."       │
 └─────────────────────────────────────────────────────────────────────┘

 14:25 PM  💬 Web Chat (Sarah switches channel)  CONTINUATION
 ┌─────────────────────────────────────────────────────────────────────┐
 │ Sarah: "I also emailed about this - my delivery is stuck"          │
 │                                                                     │
 │ 🔗 SYSTEM: Thread merged with email conversation                   │
 │                                                                     │
 │ Marcus (Agent): "Hi Sarah! I already see your email about          │
 │   order #ORD-7392. I'm contacting DHL right now.                   │
 │   The delivery exception is due to an address issue —              │
 │   it shows 'business closed'. Can you confirm the address?"        │
 │                                                                     │
 │ Sarah: "Oh! I used my office address. Can you redirect to          │
 │         my home: 456 Oak St, Austin TX 78701?"                     │
 │                                                                     │
 │ Marcus: "Done! ✅ Redirected to your home address.                  │
 │   New ETA: Tomorrow by 12 PM. I've also added a $15 credit        │
 │   to your account for the inconvenience."                           │
 │                                                                     │
 │ ✅ RESOLVED by Agent | AI-Assisted | Time: 4 minutes               │
 └─────────────────────────────────────────────────────────────────────┘

 DAY 4 — April 2, 2026
 ──────────────────────

 11:45 AM  📱 WhatsApp (Proactive)              INTENT: follow_up
 ┌─────────────────────────────────────────────────────────────────────┐
 │ 🤖 AI (Auto): "Hi Sarah! Great news — your Dell XPS 15            │
 │   was just delivered to 456 Oak St. 📦                             │
 │   Hope your presentation goes great!                                │
 │   If you need any setup help, just message us."                     │
 │                                                                     │
 │ Sarah: "Got it, thank you so much! 🙌"                             │
 │                                                                     │
 │ ✅ PROACTIVE FOLLOW-UP | AI-driven | CSAT likely: HIGH             │
 └─────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════
 THREAD SUMMARY: 3 interactions across 3 channels, 1 agent touch,
                 resolved in <24h after escalation. $15 credit issued.
═══════════════════════════════════════════════════════════════════════════
```

---

## 2. Agent Dashboard Wireframe

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  🟢 DARVIX Agent Dashboard         Marcus Chen (Shipping)    🔔 3   ⚙️  👤    │
├──────────────────┬──────────────────────────────────────┬────────────────────────┤
│                  │                                      │                        │
│  ACTIVE QUEUE    │  CONVERSATION — Sarah Johnson        │  CUSTOMER CONTEXT      │
│  ───────────     │  ──────────────────────────          │  ────────────────      │
│                  │                                      │                        │
│  ⬤ Sarah J.     │  Channel: 💬 Web Chat (via 📧 Email) │  Sarah Johnson         │
│  🔴 Urgency: 4  │                                      │  📱 +1-512-555-0147    │
│  delivery_issue  │  ┌──────────────────────────────┐   │  📧 sarah@company.com  │
│  💬 Web Chat     │  │ 📧 14:22 - Email received     │   │  🏢 Austin, TX         │
│  2 min ago       │  │ "My laptop was supposed..."   │   │                        │
│                  │  │                                │   │  ── HISTORY ──         │
│  ⬤ Mike R.      │  │ 💬 14:25 - Chat started        │   │  Orders: 12            │
│  🟡 Urgency: 2  │  │ "I also emailed about this"   │   │  Lifetime: $4,280      │
│  billing_inquiry │  │                                │   │  CSAT avg: 4.2/5       │
│  📧 Email       │  │ 👤 14:26 - You                 │   │  Segment: Premium      │
│  8 min ago       │  │ "Hi Sarah! I already see..."  │   │                        │
│                  │  │                                │   │  ── RECENT ──          │
│  ⬤ Lisa K.      │  │ 💬 14:27 - Sarah               │   │  Mar 30 📱 order_status│
│  🟡 Urgency: 2  │  │ "Can you redirect to home?"   │   │    → AI resolved ✅    │
│  return_request  │  │                                │   │  Mar 15 📧 billing     │
│  📱 WhatsApp    │  └──────────────────────────────┘   │    → Agent resolved ✅  │
│  12 min ago      │                                      │  Feb 22 💬 product_q    │
│                  │  ┌──────────────────────────────┐   │    → AI resolved ✅    │
│  ─── PENDING ─── │  │  Type a message...        📎 🔗│   │                        │
│                  │  └──────────────────────────────┘   │  ── SENTIMENT ──       │
│  ○ Tom H.       │                                      │  Current: 😟 -0.7      │
│  🟢 Urgency: 1  │  ┌──────────────────────────────┐   │  Trend: ↘ declining    │
│  general_inquiry │  │  🤖 AI SUGGESTIONS            │   │                        │
│  📧 Email       │  │                                │   │  ── AI ANALYSIS ──     │
│  34 min ago      │  │  💡 Suggested Response:        │   │  Intent: delivery_issue│
│                  │  │  "Done! ✅ I've redirected      │   │  Confidence: 0.96     │
│                  │  │  your delivery to [address].   │   │  Urgency: 4/5          │
│                  │  │  New ETA: Tomorrow by 12 PM."  │   │  Escalate: No          │
│                  │  │                                │   │                        │
│                  │  │  ⚡ Quick Actions:              │   │  ── ACTIONS LOG ──     │
│                  │  │  [Redirect Delivery]           │   │  • DHL contacted       │
│                  │  │  [Issue Credit]                │   │  • Address updated     │
│                  │  │  [Escalate to Supervisor]      │   │  • $15 credit issued   │
│                  │  │  [Create Ticket]               │   │                        │
│                  │  │                                │   │                        │
│                  │  │  [✓ Send] [✏️ Edit] [✗ Reject] │   │                        │
│                  │  └──────────────────────────────┘   │                        │
│                  │                                      │                        │
├──────────────────┴──────────────────────────────────────┴────────────────────────┤
│  📊 My Stats: Active: 4 │ Resolved Today: 18 │ Avg Handle: 4.2m │ CSAT: 4.6    │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Supervisor Dashboard Wireframe

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  🟢 DARVIX Supervisor Dashboard     Team Lead: Priya Sharma    🔔 7   ⚙️  👤  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─── REAL-TIME METRICS ─────────────────────────────────────────────────────┐ │
│  │                                                                            │ │
│  │  QUEUE HEALTH         AI PERFORMANCE        TEAM STATUS                   │ │
│  │  ────────────         ──────────────        ───────────                   │ │
│  │  In Queue: 23         Auto-Resolved: 68%    Online: 12/15                 │ │
│  │  Avg Wait: 1.2m       Accuracy: 91.3%       Avg Load: 5.2/8              │ │
│  │  SLA at Risk: 3 ⚠️    Escalation Rate: 18%  Available: 4                  │ │
│  │  Breached: 0 ✅        Confidence Avg: 0.87  On Break: 3                   │ │
│  │                                                                            │ │
│  └────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─── CHANNEL DISTRIBUTION ──────────┐  ┌─── URGENCY BREAKDOWN ─────────────┐ │
│  │                                    │  │                                    │ │
│  │  Web Chat  ████████████████ 42%    │  │  🔴 Critical (5)  ██ 3%           │ │
│  │  WhatsApp  ██████████████ 35%      │  │  🟠 High (4)      ████ 12%       │ │
│  │  Email     ████████ 18%            │  │  🟡 Medium (3)    ██████████ 35% │ │
│  │  Voice     ██ 3%                   │  │  🟢 Low (2)       ████████ 30%   │ │
│  │  Social    █ 2%                    │  │  ⚪ Minimal (1)   █████ 20%       │ │
│  │                                    │  │                                    │ │
│  └────────────────────────────────────┘  └────────────────────────────────────┘ │
│                                                                                 │
│  ┌─── AGENT PERFORMANCE ─────────────────────────────────────────────────────┐ │
│  │                                                                            │ │
│  │  Agent           Active  Resolved  AHT     CSAT   AI Assist%  Status     │ │
│  │  ─────           ──────  ────────  ───     ────   ──────────  ──────     │ │
│  │  Marcus Chen     4       18        4.2m    4.6    78%         🟢 Online  │ │
│  │  Aisha Patel     6       22        3.1m    4.8    85%         🟢 Online  │ │
│  │  David Kim       5       15        5.8m    4.3    62%         🟢 Online  │ │
│  │  Emma Wilson     3       20        3.5m    4.7    81%         🟢 Online  │ │
│  │  Carlos Ruiz     0       12        4.0m    4.5    73%         🟡 Break   │ │
│  │                                                                            │ │
│  └────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─── ALERTS & ESCALATIONS ──────────────────────────────────────────────────┐ │
│  │                                                                            │ │
│  │  ⚠️ 14:32  SLA at risk: Customer #5829 (billing_dispute) — 22 min left   │ │
│  │  ⚠️ 14:28  AI confidence low (0.52): Customer #4102 — needs human review  │ │
│  │  ⚠️ 14:15  Sentiment spike: 5 negative conversations in last 10 min      │ │
│  │  ✅ 14:10  Resolved: Priority escalation for Customer #3847               │ │
│  │                                                                            │ │
│  └────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Escalation & Routing UX Flow

### Smart Routing Decision Tree

```
                 ┌─────────────┐
                 │  INBOUND     │
                 │  MESSAGE     │
                 └──────┬──────┘
                        ▼
                 ┌─────────────┐
                 │  AI ANALYSIS │
                 │  (Intent,    │
                 │  Sentiment,  │
                 │  Urgency)    │
                 └──────┬──────┘
                        ▼
              ┌────────────────────┐
              │ Confidence ≥ 0.85  │
              │ AND Risk = LOW?    │
              └───┬────────────┬───┘
                  │YES         │NO
                  ▼            ▼
          ┌──────────┐  ┌────────────────┐
          │ AI AUTO   │  │ Urgency ≥ 4?   │
          │ RESPOND   │  └──┬──────────┬──┘
          └──────────┘     │YES       │NO
                           ▼          ▼
                   ┌────────────┐ ┌────────────────┐
                   │ PRIORITY   │ │ Confidence      │
                   │ ESCALATION │ │ ≥ 0.70?         │
                   └─────┬──────┘ └──┬──────────┬──┘
                         │           │YES       │NO
                         ▼           ▼          ▼
                   ┌──────────┐ ┌──────────┐ ┌──────────────┐
                   │ Route to │ │ AI DRAFT  │ │ FULL HUMAN   │
                   │ TOP agent│ │ + Agent   │ │ HANDLING     │
                   │ + Alert  │ │ APPROVAL  │ │ (AI assists  │
                   │ supervisor│ │          │ │  in sidebar)  │
                   └──────────┘ └──────────┘ └──────────────┘
```

### Agent Matching Algorithm

```
Incoming Conversation
        │
        ▼
┌───────────────────────────────────────────────────┐
│              AGENT MATCHING SCORE                   │
│                                                     │
│  Score = (Skill Match × 0.40)                      │
│        + (Availability × 0.25)                      │
│        + (Load Balance × 0.20)                      │
│        + (Customer History × 0.15)                  │
│                                                     │
│  Skill Match:    Agent skills vs. detected intent   │
│  Availability:   Online + not at capacity           │
│  Load Balance:   Prefer agents with fewer active    │
│  Customer Hx:    Prefer agent who served before     │
│                                                     │
│  → Route to HIGHEST SCORING agent                   │
│  → If all occupied, add to priority queue           │
│  → If wait > SLA threshold, alert supervisor        │
└─────────────────────────────────────────────────────┘
```

### Escalation Scenarios

```
┌──────────────────────────────────────────────────────────────────────┐
│                    ESCALATION MATRIX                                  │
├──────────────┬─────────────┬────────────────┬───────────────────────┤
│ Trigger      │ Action      │ Notification   │ SLA                   │
├──────────────┼─────────────┼────────────────┼───────────────────────┤
│ Urgency = 5  │ Route to    │ Supervisor     │ Response: 2 min       │
│ (Critical)   │ top agent   │ alert + SMS    │ Resolution: 1 hour    │
├──────────────┼─────────────┼────────────────┼───────────────────────┤
│ Negative     │ Flag for    │ Supervisor     │ Review within         │
│ sentiment    │ supervisor  │ dashboard      │ 15 minutes            │
│ trending ↘   │ review      │ alert          │                       │
├──────────────┼─────────────┼────────────────┼───────────────────────┤
│ Customer     │ Auto-flag   │ Agent receives │ Agent response:       │
│ asks for     │ + route up  │ full context   │ 30 seconds            │
│ manager      │             │ + AI summary   │                       │
├──────────────┼─────────────┼────────────────┼───────────────────────┤
│ AI conf.     │ Route to    │ Agent sees AI  │ Normal SLA            │
│ < 0.70       │ human agent │ analysis +     │                       │
│              │             │ suggestions    │                       │
├──────────────┼─────────────┼────────────────┼───────────────────────┤
│ 3+ channel   │ Priority    │ Supervisor +   │ Response: 1 min       │
│ switches in  │ boost +     │ retention      │ (customer is          │
│ 24 hours     │ retention   │ team alert     │  frustrated)          │
│              │ flag        │                │                       │
├──────────────┼─────────────┼────────────────┼───────────────────────┤
│ SLA at 80%   │ Auto-boost  │ Supervisor     │ Must resolve before   │
│ elapsed      │ priority    │ alert          │ SLA breach            │
└──────────────┴─────────────┴────────────────┴───────────────────────┘
```

---

## 5. Customer Self-Service UX (Web Chat Widget)

```
┌────────────────────────────┐
│  💬 DARVIX Support         │
│  ━━━━━━━━━━━━━━━━━━━━━━   │
│                            │
│  🤖 Hi Sarah! Welcome back.│
│  I see you're a Premium    │
│  customer. How can I help? │
│                            │
│  ┌──────────────────────┐  │
│  │ 📦 Track my order    │  │
│  ├──────────────────────┤  │
│  │ 💳 Billing question  │  │
│  ├──────────────────────┤  │
│  │ 🔧 Technical support │  │
│  ├──────────────────────┤  │
│  │ 💬 Other             │  │
│  └──────────────────────┘  │
│                            │
│  ┌──────────────────┐ 📎  │
│  │ Type a message...│ ➤   │
│  └──────────────────┘     │
│                            │
│  🟢 AI-powered • avg 8s   │
└────────────────────────────┘
```
