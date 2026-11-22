"""
Rotas para histórico de análises.
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone

router = APIRouter()

# Armazenamento em memória (ponytail: placeholder para banco de dados)
_history: List[dict] = []
MAX_HISTORY = 10_000


def record(result) -> None:
    """Registra um resultado de análise no histórico em memória."""
    _history.append({
        "text": result.text,
        "sentiment": result.sentiment.value,
        "confidence": result.confidence,
        "analyzed_at": datetime.now(timezone.utc),
    })
    del _history[:-MAX_HISTORY]


class HistoryEntry(BaseModel):
    """Entrada no histórico"""

    text: str
    sentiment: str
    confidence: float
    analyzed_at: datetime


class HistoryResponse(BaseModel):
    """Resposta do histórico"""

    entries: List[HistoryEntry]
    total: int


@router.get("/", response_model=HistoryResponse)
async def get_history(limit: Optional[int] = Query(default=50, ge=0)):
    """
    Retorna histórico de análises.

    - **limit**: Número máximo de entradas (padrão: 50)
    """
    entries = _history[-limit:] if limit else _history
    return HistoryResponse(entries=entries, total=len(_history))


@router.post("/clear")
async def clear_history():
    """Limpa o histórico"""
    removed = len(_history)
    _history.clear()
    return {"message": "Histórico limpo", "entries_removed": removed}


@router.get("/stats")
async def get_stats():
    """Retorna estatísticas do histórico"""
    if not _history:
        return {
            "total": 0,
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "avg_confidence": 0,
        }

    total = len(_history)
    positive = sum(1 for e in _history if e["sentiment"] == "positive")
    negative = sum(1 for e in _history if e["sentiment"] == "negative")
    neutral = sum(1 for e in _history if e["sentiment"] == "neutral")
    avg_conf = sum(e["confidence"] for e in _history) / total

    return {
        "total": total,
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "avg_confidence": round(avg_conf, 3),
    }