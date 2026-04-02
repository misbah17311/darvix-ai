# DARVIX — AI-Powered Omnichannel Customer Experience Platform

## Architecture

```
backend/
├── app/
│   ├── main.py                 # FastAPI entry point
│   ├── config.py               # Settings & environment
│   ├── models/                 # SQLAlchemy / Pydantic models
│   ├── api/                    # REST API routes
│   ├── services/               # Business logic
│   │   ├── ai/                 # AI engine (intent, sentiment, urgency, response)
│   │   ├── channels/           # Channel adapters (WhatsApp, email, web chat)
│   │   ├── routing/            # Smart routing & escalation
│   │   └── customer/           # Customer context & identity resolution
│   ├── core/                   # Message bus, auth, middleware
│   └── db/                     # Database setup & migrations
├── tests/
├── requirements.txt
├── Dockerfile
└── docker-compose.yml

frontend/
├── src/
│   ├── components/             # React components
│   │   ├── Dashboard/          # Agent dashboard
│   │   ├── Chat/               # Chat interface
│   │   └── Analytics/          # Supervisor analytics
│   ├── hooks/                  # Custom React hooks
│   ├── services/               # API client
│   └── App.tsx
├── package.json
└── Dockerfile
```

## Quick Start

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Documentation

- [PRD](docs/01_PRD.md)
- [AI Blueprint](docs/02_AI_Blueprint.md)
- [Wireframes & Journey Maps](docs/03_Wireframes_Journey_Maps.md)
- [Business Case](docs/04_Business_Case.md)
