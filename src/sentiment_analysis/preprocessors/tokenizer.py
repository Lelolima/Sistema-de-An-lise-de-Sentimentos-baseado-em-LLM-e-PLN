"""
Tokenização de texto para PLN.
"""

from typing import List, Optional
from loguru import logger


class Tokenizer:
    """
    Tokenizador de texto com suporte a múltiplos backends.

    Usa spaCy quando disponível, fallback para tokenização simples.
    """

    def __init__(self, model: Optional[str] = None):
        """
        Inicializa o tokenizador.

        Args:
            model: Modelo spaCy (ex: 'pt_core_news_sm'). Opcional.
        """
        self.model = model
        self._nlp = None
        self._try_load_spacy()

    def _try_load_spacy(self) -> None:
        """Tenta carregar modelo spaCy"""
        if self.model is None:
            return

        try:
            import spacy

            self._nlp = spacy.load(self.model, disable=["parser", "ner"])
            logger.info(f"Modelo spaCy carregado: {self.model}")
        except (ImportError, OSError) as e:
            logger.warning(
                f"Não foi possível carregar spaCy ('{self.model}'): {e}. "
                "Usando tokenização simples."
            )
            self._nlp = None

    def tokenize(self, text: str) -> List[str]:
        """
        Tokeniza um texto.

        Args:
            text: Texto para tokenizar

        Returns:
            List[str]: Lista de tokens
        """
        if not text:
            return []

        if self._nlp is not None:
            doc = self._nlp(text)
            return [token.text for token in doc if not token.is_space]

        # Fallback: tokenização simples por palavra
        import re

        tokens = re.findall(r"\b[\w]+\b", text.lower(), re.UNICODE)
        return tokens

    def tokenize_with_metadata(
        self, text: str
    ) -> dict[str, list[str]]:
        """
        Tokeniza e retorna metadados.

        Args:
            text: Texto para tokenizar

        Returns:
            dict com tokens e informações adicionais
        """
        if not text:
            return {"tokens": [], "count": 0}

        if self._nlp is not None:
            doc = self._nlp(text)
            return {
                "tokens": [t.text for t in doc if not t.is_space],
                "lemmas": [t.lemma_ for t in doc if not t.is_space],
                "pos_tags": [(t.text, t.pos_) for t in doc if not t.is_space],
                "count": len([t for t in doc if not t.is_space]),
            }

        tokens = self.tokenize(text)
        return {
            "tokens": tokens,
            "lemmas": tokens,  # ponytail: sem lematização no fallback
            "pos_tags": [(t, "UNK") for t in tokens],
            "count": len(tokens),
        }