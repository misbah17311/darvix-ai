#!/bin/bash
# =============================================================
# DARVIX Platform — Full Test Script
# Tests all channels, AI routing, agent actions, and dashboard
# =============================================================

BASE_URL="${1:-https://darvix-ai.onrender.com}"
echo "🔧 Testing DARVIX at: $BASE_URL"
echo ""

# ---- 1. Health Check ----
echo "=== 1. Health Check ==="
curl -s "$BASE_URL/api/health" | python3 -m json.tool 2>/dev/null || echo "(no json.tool)"
echo ""

# ---- 2. Login as Demo Agent ----
echo "=== 2. Login (demo@darvix.ai / demo1234) ==="
TOKEN=$(curl -s -X POST "$BASE_URL/api/agents/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@darvix.ai","password":"demo1234"}' | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token','LOGIN_FAILED'))" 2>/dev/null)

if [ "$TOKEN" = "LOGIN_FAILED" ] || [ -z "$TOKEN" ]; then
  echo "❌ Login failed. Is the server running?"
  exit 1
fi
echo "✅ Logged in. Token: ${TOKEN:0:20}..."
echo ""

# ---- 3. Check Dashboard Metrics (before) ----
echo "=== 3. Dashboard Metrics (before messages) ==="
curl -s "$BASE_URL/api/dashboard/metrics" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool 2>/dev/null
echo ""

# ---- 4. Simulate Customer Messages (3 channels) ----
echo "=== 4a. WebChat — Billing complaint ==="
curl -s -X POST "$BASE_URL/api/messages/inbound/webchat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "cust-web-001",
    "email": "alice@example.com",
    "message": "I was charged twice on my credit card for order #12345. I need a refund immediately. This is very frustrating."
  }' | python3 -m json.tool 2>/dev/null
echo ""

echo "=== 4b. WhatsApp — Angry technical issue (high urgency) ==="
curl -s -X POST "$BASE_URL/api/messages/inbound/whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "entry": [{"changes": [{"value": {
      "messages": [{"from": "+1555000111", "type": "text", "text": {"body": "My internet has been down for 6 hours! I work from home and I am losing money every minute. Fix this NOW or I am switching providers!!"}, "id": "wa-msg-001", "timestamp": "1712345678"}],
      "contacts": [{"profile": {"name": "Bob Wilson"}}]
    }}]}]
  }' | python3 -m json.tool 2>/dev/null
echo ""

echo "=== 4c. Email — Upgrade inquiry (low urgency, positive) ==="
curl -s -X POST "$BASE_URL/api/messages/inbound/email" \
  -H "Content-Type: application/json" \
  -d '{
    "from_email": "carol@example.com",
    "subject": "Interested in Enterprise plan",
    "text_body": "Hello! I am currently on the Basic plan and loving the product. I would like to learn about upgrading to Enterprise. Could you share the pricing and migration steps?"
  }' | python3 -m json.tool 2>/dev/null
echo ""

echo "=== 4d. WebChat — Password reset (simple, auto-resolvable) ==="
curl -s -X POST "$BASE_URL/api/messages/inbound/webchat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "cust-web-002",
    "email": "dave@example.com",
    "message": "How do I reset my password?"
  }' | python3 -m json.tool 2>/dev/null
echo ""

echo "=== 4e. WhatsApp — Cancellation request (churn risk) ==="
curl -s -X POST "$BASE_URL/api/messages/inbound/whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "entry": [{"changes": [{"value": {
      "messages": [{"from": "+1555000222", "type": "text", "text": {"body": "I want to cancel my subscription. The service has been terrible lately and I found a better alternative."}, "id": "wa-msg-002", "timestamp": "1712345700"}],
      "contacts": [{"profile": {"name": "Eve Martinez"}}]
    }}]}]
  }' | python3 -m json.tool 2>/dev/null
echo ""

# ---- 5. Check Dashboard Metrics (after) ----
echo "=== 5. Dashboard Metrics (after messages) ==="
curl -s "$BASE_URL/api/dashboard/metrics" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool 2>/dev/null
echo ""

# ---- 6. List All Conversations ----
echo "=== 6. List Conversations ==="
CONVERSATIONS=$(curl -s "$BASE_URL/api/conversations" \
  -H "Authorization: Bearer $TOKEN")
echo "$CONVERSATIONS" | python3 -m json.tool 2>/dev/null
echo ""

# ---- 7. Get First Conversation Detail ----
FIRST_ID=$(echo "$CONVERSATIONS" | python3 -c "import sys,json; data=json.load(sys.stdin); print(data[0]['id'] if data else 'NONE')" 2>/dev/null)
if [ "$FIRST_ID" != "NONE" ] && [ -n "$FIRST_ID" ]; then
  echo "=== 7. Conversation Detail: $FIRST_ID ==="
  curl -s "$BASE_URL/api/conversations/$FIRST_ID" \
    -H "Authorization: Bearer $TOKEN" | python3 -m json.tool 2>/dev/null
  echo ""

  # ---- 8. Agent sends a reply ----
  echo "=== 8. Agent Reply ==="
  AGENT_ID=$(curl -s "$BASE_URL/api/agents/me" \
    -H "Authorization: Bearer $TOKEN" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null)

  curl -s -X POST "$BASE_URL/api/messages/agent-send/$FIRST_ID" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d "{\"content\": \"I apologize for the inconvenience. Let me look into this right away and get it resolved for you.\", \"agent_id\": \"$AGENT_ID\"}" | python3 -m json.tool 2>/dev/null
  echo ""

  # ---- 9. Resolve the conversation ----
  echo "=== 9. Resolve Conversation ==="
  curl -s -X POST "$BASE_URL/api/conversations/$FIRST_ID/resolve" \
    -H "Authorization: Bearer $TOKEN" | python3 -m json.tool 2>/dev/null
  echo ""
fi

# ---- 10. Final Metrics ----
echo "=== 10. Final Dashboard Metrics ==="
curl -s "$BASE_URL/api/dashboard/metrics" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool 2>/dev/null
echo ""

echo "============================================"
echo "✅ Test complete! Open $BASE_URL in your browser."
echo "   Login: demo@darvix.ai / demo1234"
echo "   You should see conversations in the queue."
echo "============================================"
