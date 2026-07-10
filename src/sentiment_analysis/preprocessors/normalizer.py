"""
Normalização de texto para PLN.
"""

import re
import unicodedata
from typing import Optional


class Normalizer:
    """
    Normalização de texto para análise de sentimentos.

    Remove acentos, normaliza caracteres especiais, e padroniza o texto.
    """

    def __init__(
        self,
        remove_accents: bool = True,
        normalize_repeated_chars: bool = True,
        max_repeated_chars: int = 2,
        normalize_numbers: bool = False,
    ):
        """
        Inicializa o normalizador.

        Args:
            remove_accents: Remove acentos (ex: "ação" -> "acao")
            normalize_repeated_chars: Normaliza caracteres repetidos (ex: "oooi" -> "ooi")
            max_repeated_chars: Máximo de caracteres repetidos consecutivos
            normalize_numbers: Substitui números por placeholder
        """
        self.remove_accents = remove_accents
        self.normalize_repeated_chars = normalize_repeated_chars
        self.max_repeated_chars = max_repeated_chars
        self.normalize_numbers = normalize_numbers

    def normalize(self, text: str) -> str:
        """
        Normaliza um texto.

        Args:
            text: Texto original

        Returns:
            str: Texto normalizado
        """
        if not text:
            return ""

        result = text

        # Remove acentos
        if self.remove_accents:
            result = self._remove_accents(result)

        # Normaliza caracteres repetidos
        if self.normalize_repeated_chars:
            result = self._normalize_repeated_chars(result)

        # Normaliza números
        if self.normalize_numbers:
            result = re.sub(r"\d+", "<NUM>", result)

        return result

    def _remove_accents(self, text: str) -> str:
        """Remove acentos do texto"""
        nfkd = unicodedata.normalize("NFKD", text)
        return "".join(
            c for c in nfkd if unicodedata.category(c) != "Mn"
        )

    def _normalize_repeated_chars(self, text: str) -> str:
        """
        Normaliza caracteres repetidos.

        Ex: "goooooosto" -> "goosto", "ameeeeeei" -> "ameei"
        """
        pattern = r"(.)\1{" + str(self.max_repeated_chars) + r",}"
        replacement = r"\1" * self.max_repeated_chars
        return re.sub(pattern, replacement, text)

    def normalize_batch(self, texts: list[str]) -> list[str]:
        """
        Normaliza uma lista de textos.

        Args:
            texts: Lista de textos

        Returns:
            list[str]: Textos normalizados
        """
        return [self.normalize(text) for text in texts]