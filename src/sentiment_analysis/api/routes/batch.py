"""
Rotas para análise em lote.
"""

from collections import Counter
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

from ..models.sentiment_analyzer import SentimentAnalyzer
from ..models.base_model import Sentiment

router = APIRouter()

# Cache de analisadores
_analyzers: dict[str, SentimentAnalyzer] = {}


def get_analyzer(model: str = "vader") -> SentimentAnalyzer:
    """Retorna ou cria um analisador (singleton por modelo)"""
    if model not in _analyzers:
        _analyzers[model] = SentimentAnalyzer(model=model)
    return _analyzers[model]


class BatchAnalyzeRequest(BaseModel):
    """Requisição para análise em lote"""

    texts: List[str] = Field(..., description="Lista de textos para analisar")
    model: Optional[str] = Field(default="vader", description="Modelo a usar")
    batch_size: Optional[int] = Field(default=100, description="Tamanho do batch")


class AnalyzeResult(BaseModel):
    """Resultado de uma análise individual"""

    index: int
    text: str
    sentiment: str
    confidence: float
    scores: dict[str, float]


class BatchAnalyzeResponse(BaseModel):
    """Resposta da análise em lote"""

    total: int
    results: List[AnalyzeResult]
    summary: dict[str, int]
    model: str


@router.post("/", response_model=BatchAnalyzeResponse)
async def analyze_batch(request: BatchAnalyzeRequest):
    """
    Analisa múltiplos textos em lote.

    - **texts**: Lista de textos (máx 1000)
    - **model**: Modelo a usar (vader, bert)
    - **batch_size**: Tamanho do batch para processamento
    """
    if len(request.texts) > 1000:
        raise HTTPException(status_code=400, detail="Máximo de 1000 textos por lote")

    try:
        analyzer = get_analyzer(request.model)
        results = analyzer.analyze_batch(request.texts)

        # Converte resultados
        analyzed = [
            AnalyzeResult(
                index=i,
                text=r.text,
                sentiment=r.sentiment.value,
                confidence=r.confidence,
                scores=r.scores,
            )
            for i, r in enumerate(results)
        ]

        # Resumo (ponytail: simplificado com Counter)
        summary = dict(Counter(r.sentiment.value for r in results))
        # Garante todas as chaves presentes
        for key in ["positive", "negative", "neutral"]:
            summary.setdefault(key, 0)

        return BatchAnalyzeResponse(
            total=len(results),
            results=analyzed,
            summary=summary,
            model=results[0].model_name if results else request.model,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na análise em lote: {str(e)}")