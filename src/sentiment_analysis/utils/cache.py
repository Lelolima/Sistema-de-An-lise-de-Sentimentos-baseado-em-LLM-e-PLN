"""
Cache simples para resultados de análises.
"""

import hashlib
from typing import Any, Dict, Optional
from datetime import datetime, timedelta
from loguru import logger


class Cache:
    """
    Cache em memória com expiração.

    ponytail: Implementação minimalista - usar Redis em produção.
    """

    def __init__(self, ttl_seconds: int = 3600):
        """
        Inicializa o cache.

        Args:
            ttl_seconds: Tempo de vida das entradas (segundos)
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._ttl = timedelta(seconds=ttl_seconds)
        logger.info(f"Cache inicializado com TTL={ttl_seconds}s")

    def _make_key(self, text: str, model: str) -> str:
        """Cria chave única para o cache"""
        content = f"{model}:{text}"
        return hashlib.md5(content.encode()).hexdigest()

    def get(self, text: str, model: str) -> Optional[Any]:
        """
        Obtém valor do cache.

        Args:
            text: Texto analisado
            model: Modelo usado

        Returns:
            Valor em cache ou None
        """
        key = self._make_key(text, model)
        entry = self._cache.get(key)

        if entry is None:
            return None

        # Verifica expiração
        if datetime.now() > entry["expires_at"]:
            del self._cache[key]
            return None

        return entry["value"]

    def set(self, text: str, model: str, value: Any) -> None:
        """
        Armazena valor no cache.

        Args:
            text: Texto analisado
            model: Modelo usado
            value: Valor a armazenar
        """
        key = self._make_key(text, model)
        self._cache[key] = {
            "value": value,
            "expires_at": datetime.now() + self._ttl,
            "created_at": datetime.now(),
        }

    def clear(self) -> int:
        """
        Limpa o cache.

        Returns:
            Número de entradas removidas
        """
        count = len(self._cache)
        self._cache.clear()
        logger.info(f"Cache limpo: {count} entradas removidas")
        return count

    def cleanup_expired(self) -> int:
        """
        Remove entradas expiradas.

        Returns:
            Número de entradas removidas
        """
        now = datetime.now()
        expired = [k for k, v in self._cache.items() if now > v["expires_at"]]

        for key in expired:
            del self._cache[key]

        if expired:
            logger.info(f"Cleanup: {len(expired)} entradas expiradas removidas")

        return len(expired)

    @property
    def size(self) -> int:
        """Retorna número de entradas no cache"""
        return len(self._cache)