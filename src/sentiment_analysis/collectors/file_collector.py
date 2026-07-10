"""
Coletor de arquivos locais (CSV, TXT, JSON, Excel).
"""

import csv
import json
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional
from datetime import datetime

from .base_collector import BaseCollector, CollectorConfig, CollectedData


class FileCollector(BaseCollector):
    """
    Coletor de arquivos locais.

    Suporta:
    - CSV (.csv)
    - Texto (.txt)
    - JSON (.json, .jsonl)
    - Excel (.xlsx, .xls)
    """

    def __init__(self, config: Optional[CollectorConfig] = None):
        if config is None:
            config = CollectorConfig(source_name="file")
        super().__init__(config)
        self._current_file: Optional[str] = None

    def connect(self) -> bool:
        """Verifica se o diretório base existe"""
        base_dir = self.config.extra_params.get("base_dir", ".")
        path = Path(base_dir)
        if not path.exists():
            raise FileNotFoundError(f"Diretório não encontrado: {base_dir}")
        return True

    def disconnect(self) -> None:
        """Limpa estado do coletor"""
        self._current_file = None

    def collect(
        self, file_path: str, text_column: str = "text", **kwargs
    ) -> Generator[CollectedData, None, None]:
        """
        Coleta dados de um arquivo.

        Args:
            file_path: Caminho do arquivo
            text_column: Nome da coluna contendo o texto (para CSV/Excel)
            **kwargs: Parâmetros adicionais

        Yields:
            CollectedData: Dados coletados
        """
        path = Path(file_path)
        self._current_file = str(path)

        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        suffix = path.suffix.lower()

        if suffix == ".csv":
            yield from self._collect_csv(path, text_column)
        elif suffix == ".txt":
            yield from self._collect_txt(path)
        elif suffix in [".json", ".jsonl"]:
            yield from self._collect_json(path, text_column)
        elif suffix in [".xlsx", ".xls"]:
            yield from self._collect_excel(path, text_column)
        else:
            raise ValueError(f"Formato não suportado: {suffix}")

    def _collect_csv(
        self, path: Path, text_column: str
    ) -> Generator[CollectedData, None, None]:
        """Coleta de arquivo CSV"""
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                text = row.get(text_column, "")
                if text:
                    yield CollectedData(
                        text=text,
                        source=f"file:{path}",
                        collected_at=datetime.now(),
                        metadata=dict(row),
                    )

    def _collect_txt(
        self, path: Path
    ) -> Generator[CollectedData, None, None]:
        """Coleta de arquivo TXT (uma linha por texto)"""
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                text = line.strip()
                if text:
                    yield CollectedData(
                        text=text,
                        source=f"file:{path}",
                        collected_at=datetime.now(),
                    )

    def _collect_json(
        self, path: Path, text_column: str
    ) -> Generator[CollectedData, None, None]:
        """Coleta de arquivo JSON/JSONL"""
        with open(path, "r", encoding="utf-8") as f:
            if path.suffix == ".jsonl":
                for line in f:
                    data = json.loads(line)
                    text = data.get(text_column, "")
                    if text:
                        yield CollectedData(
                            text=text,
                            source=f"file:{path}",
                            collected_at=datetime.now(),
                            metadata=data,
                        )
            else:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        text = item.get(text_column, "")
                        if text:
                            yield CollectedData(
                                text=text,
                                source=f"file:{path}",
                                collected_at=datetime.now(),
                                metadata=item,
                            )

    def _collect_excel(
        self, path: Path, text_column: str
    ) -> Generator[CollectedData, None, None]:
        """Coleta de arquivo Excel"""
        try:
            import pandas as pd

            df = pd.read_excel(path)
            if text_column not in df.columns:
                raise ValueError(f"Coluna '{text_column}' não encontrada no Excel")

            for _, row in df.iterrows():
                text = row.get(text_column, "")
                if text and isinstance(text, str):
                    yield CollectedData(
                        text=text,
                        source=f"file:{path}",
                        collected_at=datetime.now(),
                        metadata=row.to_dict(),
                    )
        except ImportError:
            raise ImportError("Instale 'openpyxl' para ler arquivos Excel")

    def collect_batch(
        self, file_paths: List[str], **kwargs
    ) -> List[CollectedData]:
        """
        Coleta dados de múltiplos arquivos.

        Args:
            file_paths: Lista de caminhos de arquivos
            **kwargs: Parâmetros adicionais

        Returns:
            List[CollectedData]: Dados coletados
        """
        results = []
        for path in file_paths:
            for item in self.collect(path, **kwargs):
                results.append(item)
        return results