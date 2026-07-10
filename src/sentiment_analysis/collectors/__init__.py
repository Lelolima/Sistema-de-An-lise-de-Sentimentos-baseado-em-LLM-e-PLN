"""
Módulos de coleta de dados de diferentes fontes.
"""

from .base_collector import BaseCollector, CollectorConfig
from .file_collector import FileCollector

__all__ = ["BaseCollector", "CollectorConfig", "FileCollector"]