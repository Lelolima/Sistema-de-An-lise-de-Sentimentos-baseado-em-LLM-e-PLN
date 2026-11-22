"""Modelo transformer via Hugging Face ``transformers`` (opcional).

Requer ``pip install transformers torch``; o modelo é baixado do Hugging Face Hub
na primeira execução. Nome configurável por ``BERT_MODEL_NAME``.
"""

from __future__ import annotations

import os

from .base_model import BaseSentimentModel, Sentiment, SentimentResult

DEFAULT_BERT_MODEL = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

_LABELS = {
    "positive": Sentiment.POSITIVE, "pos": Sentiment.POSITIVE, "label_2": Sentiment.POSITIVE,
    "negative": Sentiment.NEGATIVE, "neg": Sentiment.NEGATIVE, "label_0": Sentiment.NEGATIVE,
    "neutral": Sentiment.NEUTRAL, "neu": Sentiment.NEUTRAL, "label_1": Sentiment.NEUTRAL,
}


class BertModel(BaseSentimentModel):
    """Classificador transformer multilíngue (inclui português)."""

    name = "bert"

    def __init__(self, model_name: str | None = None):
        try:
            from transformers import pipeline
        except ImportError as exc:
            raise RuntimeError(
                "Modelo 'bert' requer 'transformers' e 'torch' instalados"
            ) from exc
        self.model_name = model_name or os.getenv("BERT_MODEL_NAME", DEFAULT_BERT_MODEL)
        self._pipe = pipeline("sentiment-analysis", model=self.model_name, top_k=None)

    def predict(self, text: str) -> SentimentResult:
        """Retorna o rótulo de maior score."""
        out = self._pipe(text, truncation=True)
        rows = out[0] if out and isinstance(out[0], list) else out
        scores = {_LABELS.get(r["label"].lower(), Sentiment.NEUTRAL).value: float(r["score"])
                  for r in rows}
        best = max(scores, key=scores.get)
        return SentimentResult(text=text, sentiment=Sentiment(best), confidence=scores[best],
                               scores=scores, model_name=self.name)
