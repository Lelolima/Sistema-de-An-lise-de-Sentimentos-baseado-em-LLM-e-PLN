"""
Limpeza de texto para análise de sentimentos.
"""

import re
from typing import Optional


class TextCleaner:
    """
    Limpeza de texto para pré-processamento em análise de sentimentos.

    Remove caracteres indesejados, URLs, mentions, e normaliza whitespace.
    """

    def __init__(
        self,
        remove_urls: bool = True,
        remove_mentions: bool = True,
        remove_hashtags: bool = False,
        remove_emojis: bool = False,
        lowercase: bool = True,
        strip_whitespace: bool = True,
    ):
        """
        Inicializa o limpador de texto.

        Args:
            remove_urls: Remove URLs (http://, https://)
            remove_mentions: Remove @menções
            remove_hashtags: Remove #hashtags
            remove_emojis: Remove emojis
            lowercase: Converte para minúsculas
            strip_whitespace: Remove whitespace extra
        """
        self.remove_urls = remove_urls
        self.remove_mentions = remove_mentions
        self.remove_hashtags = remove_hashtags
        self.remove_emojis = remove_emojis
        self.lowercase = lowercase
        self.strip_whitespace = strip_whitespace

        # Compila regex patterns (ponytail: otimização simples)
        self._url_pattern = re.compile(
            r"https?://\S+|www\.\S+", re.IGNORECASE
        )
        self._mention_pattern = re.compile(r"@\w+")
        self._hashtag_pattern = re.compile(r"#\w+")
        self._emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # Emoticons
            "\U0001F300-\U0001F5FF"  # Símbolos e pictogramas
            "\U0001F680-\U0001F6FF"  # Transporte e símbolos
            "\U0001F1E0-\U0001F1FF"  # Flags
            "]+",
            flags=re.UNICODE,
        )
        self._whitespace_pattern = re.compile(r"\s+")

    def clean(self, text: str) -> str:
        """
        Limpa o texto aplicando todas as transformações configuradas.

        Args:
            text: Texto original

        Returns:
            str: Texto limpo
        """
        if not text:
            return ""

        result = text

        # Remove URLs
        if self.remove_urls:
            result = self._url_pattern.sub("", result)

        # Remove mentions
        if self.remove_mentions:
            result = self._mention_pattern.sub("", result)

        # Remove hashtags
        if self.remove_hashtags:
            result = self._hashtag_pattern.sub("", result)

        # Remove emojis
        if self.remove_emojis:
            result = self._emoji_pattern.sub("", result)

        # Lowercase
        if self.lowercase:
            result = result.lower()

        # Strip whitespace
        if self.strip_whitespace:
            result = self._whitespace_pattern.sub(" ", result).strip()

        return result

    def clean_batch(self, texts: list[str]) -> list[str]:
        """
        Limpa uma lista de textos.

        Args:
            texts: Lista de textos

        Returns:
            list[str]: Textos limpos
        """
        return [self.clean(text) for text in texts]