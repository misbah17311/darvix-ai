"""
Knowledge Base service — ChromaDB vector store for RAG.

Stores and retrieves:
- Knowledge base articles
- Past conversation summaries
- Product/policy documents
"""

import logging
import chromadb
from chromadb.config import Settings as ChromaSettings
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

_chroma_client = None
_kb_collection = None
_conversations_collection = None


def get_chroma_client():
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.Client(ChromaSettings(
            persist_directory=settings.chroma_persist_dir,
            anonymized_telemetry=False,
        ))
    return _chroma_client


def get_kb_collection():
    global _kb_collection
    if _kb_collection is None:
        client = get_chroma_client()
        _kb_collection = client.get_or_create_collection(
            name="knowledge_base",
            metadata={"description": "Company knowledge base articles and policies"},
        )
    return _kb_collection


def get_conversations_collection():
    global _conversations_collection
    if _conversations_collection is None:
        client = get_chroma_client()
        _conversations_collection = client.get_or_create_collection(
            name="past_conversations",
            metadata={"description": "Summaries of past resolved conversations"},
        )
    return _conversations_collection


async def search_knowledge_base(query: str, n_results: int = 5) -> list[str]:
    """Search the knowledge base for relevant articles."""
    try:
        collection = get_kb_collection()
        if collection.count() == 0:
            return []

        results = collection.query(query_texts=[query], n_results=min(n_results, collection.count()))
        return results.get("documents", [[]])[0]
    except Exception as e:
        logger.error(f"KB search failed: {e}")
        return []


async def search_past_conversations(query: str, n_results: int = 3) -> list[str]:
    """Search past conversation summaries for similar issues."""
    try:
        collection = get_conversations_collection()
        if collection.count() == 0:
            return []

        results = collection.query(query_texts=[query], n_results=min(n_results, collection.count()))
        return results.get("documents", [[]])[0]
    except Exception as e:
        logger.error(f"Conversation search failed: {e}")
        return []


async def add_kb_article(article_id: str, content: str, metadata: dict | None = None):
    """Add or update a knowledge base article."""
    collection = get_kb_collection()
    collection.upsert(
        ids=[article_id],
        documents=[content],
        metadatas=[metadata or {}],
    )


async def add_conversation_summary(conversation_id: str, summary: str, metadata: dict | None = None):
    """Store a resolved conversation summary for future RAG retrieval."""
    collection = get_conversations_collection()
    collection.upsert(
        ids=[conversation_id],
        documents=[summary],
        metadatas=[metadata or {}],
    )
