"""
Sistema de Análise de Sentimentos com LLM e PLN
================================================
Pacote principal para análise de sentimentos usando Processamento de Linguagem Natural.
"""

__version__ = "0.1.0"
__author__ = "Seu Nome"

from .config import settings
from .logging_config import setup_logging

__all__ = ["settings", "setup_logging"]