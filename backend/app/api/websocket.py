"""
WebSocket endpoint for real-time agent dashboard updates.
"""

import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.auth import decode_token

logger = logging.getLogger(__name__)
router = APIRouter()

# Active WebSocket connections: agent_id -> WebSocket
active_connections: dict[str, WebSocket] = {}


@router.websocket("/ws/agent/{token}")
async def agent_websocket(websocket: WebSocket, token: str):
    """
    WebSocket connection for agents to receive real-time updates:
    - New conversation assignments
    - Customer messages
    - AI suggestions
    - Queue updates
    """
    try:
        payload = decode_token(token)
        agent_id = payload.get("sub")
    except Exception:
        await websocket.close(code=4001, reason="Invalid token")
        return

    await websocket.accept()
    active_connections[agent_id] = websocket
    logger.info(f"Agent {agent_id} connected via WebSocket")

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            # Handle agent actions via WebSocket
            msg_type = message.get("type")
            if msg_type == "heartbeat":
                await websocket.send_json({"type": "heartbeat_ack"})
            elif msg_type == "typing":
                # Broadcast typing indicator to customer
                pass

    except WebSocketDisconnect:
        active_connections.pop(agent_id, None)
        logger.info(f"Agent {agent_id} disconnected")
    except Exception as e:
        active_connections.pop(agent_id, None)
        logger.error(f"WebSocket error for agent {agent_id}: {e}")


async def notify_agent(agent_id: str, data: dict):
    """Send a real-time notification to a specific agent."""
    ws = active_connections.get(agent_id)
    if ws:
        try:
            await ws.send_json(data)
        except Exception:
            active_connections.pop(agent_id, None)


async def broadcast_to_all(data: dict):
    """Broadcast to all connected agents (e.g., queue updates)."""
    disconnected = []
    for agent_id, ws in active_connections.items():
        try:
            await ws.send_json(data)
        except Exception:
            disconnected.append(agent_id)
    for agent_id in disconnected:
        active_connections.pop(agent_id, None)
