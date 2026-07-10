"""
Rotas para análise de sentimentos.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from loguru import logger

from ..models.sentiment_analyzer import SentimentAnalyzer
from ..models.base_model import Sentiment

router = APIRouter()

# Cache de analisadores (ponytail: simple singleton)
_analyzers: dict[str, SentimentAnalyzer] = {}


def get_analyzer(model: str = "vader") -> SentimentAnalyzer:
    """Retorna ou cria um analisador (singleton por modelo)"""
    if model not in _analyzers:
        _analyzers[model] = SentimentAnalyzer(model=model)
    return _analyzers[model]


class AnalyzeRequest(BaseModel):
    """Requisição para análise de texto"""

    text: str = Field(..., description="Texto para analisar", min_length=1, max_length=512)
    model: Optional[str] = Field(default="vader", description="Modelo a usar")


class AnalyzeResponse(BaseModel):
    """Resposta da análise"""

    text: str
    sentiment: str
    confidence: float
    scores: dict[str, float]
    model: str


@router.post("/", response_model=AnalyzeResponse)
async def analyze_text(request: AnalyzeRequest):
    """
    Analisa o sentimento de um texto.

    - **text**: Texto para analisar (1-512 caracteres)
    - **model**: Modelo a usar (vader, bert)
    """
    try:
        analyzer = get_analyzer(request.model)
        result = analyzer.analyze(request.text)

        return AnalyzeResponse(
            text=result.text,
            sentiment=result.sentiment.value,
            confidence=result.confidence,
            scores=result.scores,
            model=result.model_name,
        )
    except Exception as e:
        logger.error(f"Erro na análise: {e}")
        raise HTTPException(status_code=500, detail=f"Erro na análise: {str(e)}")


@router.get("/models")
async def list_models():
    """Lista modelos disponíveis"""
    analyzer = SentimentAnalyzer()
    return {"models": analyzer.get_available_models()}