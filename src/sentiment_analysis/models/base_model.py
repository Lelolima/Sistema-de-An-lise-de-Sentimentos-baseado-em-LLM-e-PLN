"""Interface base e tipos dos modelos de sentimento."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


class Sentiment(str, Enum):
    """Polaridade do sentimento."""

    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


@dataclass
class SentimentResult:
    """Resultado de uma análise."""

    text: str
    sentiment: Sentiment
    confidence: float
    scores: dict[str, float] = field(default_factory=dict)
    model_name: str = ""


class BaseSentimentModel(ABC):
    """Contrato que todo modelo de sentimento implementa."""

    name: str = "base"

    @abstractmethod
    def predict(self, text: str) -> SentimentResult:
        """Analisa um texto."""

    def predict_batch(self, texts: list[str]) -> list[SentimentResult]:
        """Analisa vários textos (padrão: um a um)."""
        return [self.predict(t) for t in texts]
