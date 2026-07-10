"""
Coletor base abstrato para definição de coletores de dados.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Generator, List, Optional
from datetime import datetime


@dataclass
class CollectorConfig:
    """Configuração para coletores de dados"""

    source_name: str
    batch_size: int = 100
    max_retries: int = 3
    rate_limit: int = 100  # requisições por minuto
    timeout: int = 30

    # Campos opcionais específicos
    extra_params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CollectedData:
    """Dados coletados de uma fonte"""

    text: str
    source: str
    collected_at: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.collected_at, datetime):
            self.collected_at = datetime.now()


class BaseCollector(ABC):
    """
    Classe base abstrata para coletores de dados.

    Define a interface comum para todos os coletores (Twitter, Google Reviews,
    arquivos, etc.).
    """

    def __init__(self, config: CollectorConfig):
        self.config = config
        self._session = None

    @abstractmethod
    def connect(self) -> bool:
        """
        Estabelece conexão com a fonte de dados.

        Returns:
            bool: True se conectado com sucesso
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Fecha a conexão com a fonte de dados"""
        pass

    @abstractmethod
    def collect(self, query: str, **kwargs) -> Generator[CollectedData, None, None]:
        """
        Coleta dados da fonte.

        Args:
            query: Termo de busca ou identificador
            **kwargs: Parâmetros adicionais específicos de cada coletor

        Yields:
            CollectedData: Dados coletados
        """
        pass

    @abstractmethod
    def collect_batch(
        self, queries: List[str], **kwargs
    ) -> List[CollectedData]:
        """
        Coleta dados em lote.

        Args:
            queries: Lista de termos de busca
            **kwargs: Parâmetros adicionais

        Returns:
            List[CollectedData]: Dados coletados
        """
        results = []
        for query in queries:
            for item in self.collect(query, **kwargs):
                results.append(item)
        return results

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()