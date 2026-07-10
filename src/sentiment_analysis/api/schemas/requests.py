"""
Schema de pedidos da API.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class TextAnalysisRequest(BaseModel):
    """Pedido de análise de texto"""

    text: str = Field(..., min_length=1, max_length=1000)
    model: Optional[str] = "vader"


class TextAnalysisResponse(BaseModel):
    """Resposta de análise de texto"""

    text: str
    sentiment: str
    confidence: float
    model: str


class BatchRequest(BaseModel):
    """Pedido de análise em lote"""

    texts: List[str] = Field(..., max_items=1000)
    model: Optional[str] = "vader"