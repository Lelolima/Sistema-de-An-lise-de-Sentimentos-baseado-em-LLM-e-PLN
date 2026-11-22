"""Fachada que escolhe e executa um modelo de sentimento."""

from __future__ import annotations

from .base_model import BaseSentimentModel, SentimentResult

AVAILABLE_MODELS = {
    "vader": "Léxico VADER (inglês), leve, sem download",
    "bert": "Transformer Hugging Face (multilíngue); requer transformers + torch",
}


def _build(model: str) -> BaseSentimentModel:
    if model == "vader":
        from .vader_model import VaderModel

        return VaderModel()
    if model == "bert":
        from .bert_model import BertModel

        return BertModel()
    raise ValueError(f"Modelo desconhecido: {model!r}. Disponíveis: {sorted(AVAILABLE_MODELS)}")


class SentimentAnalyzer:
    """Ponto de entrada usado pela API, dashboard e ``main.py``."""

    def __init__(self, model: str = "vader"):
        self.model_name = model
        self._model: BaseSentimentModel | None = None

    @property
    def model(self) -> BaseSentimentModel:
        """Instancia o modelo sob demanda."""
        if self._model is None:
            self._model = _build(self.model_name)
        return self._model

    def analyze(self, text: str) -> SentimentResult:
        """Analisa um texto não vazio."""
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Texto vazio")
        return self.model.predict(text)

    def analyze_batch(self, texts: list[str]) -> list[SentimentResult]:
        """Analisa uma lista de textos (rejeita itens vazios)."""
        for t in texts:
            if not isinstance(t, str) or not t.strip():
                raise ValueError("Lote contém texto vazio")
        return self.model.predict_batch(texts)

    @staticmethod
    def get_available_models() -> dict[str, str]:
        """Modelos implementados."""
        return dict(AVAILABLE_MODELS)
