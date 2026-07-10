"""
Configuração de logging centralizada.
"""

import logging
import sys
from pathlib import Path
from loguru import logger

from .config import settings


def setup_logging() -> None:
    """
    Configura o logging para toda a aplicação.

    Usa loguru para logs estruturados com cores e formatação adequada.
    """
    # Cria diretório de logs se não existir
    log_path = Path(settings.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Remove handler padrão do loguru
    logger.remove()

    # Handler para console com cores
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.log_level,
        colorize=True,
    )

    # Handler para arquivo com rotação
    logger.add(
        settings.log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=settings.log_level,
        rotation="10 MB",
        retention="7 days",
        compression="zip",
    )

    # Configura logging padrão do Python para usar loguru
    class LoguruHandler(logging.Handler):  # ponytail: integração minimalista
        """Handler para redirecionar logging padrão para loguru"""

        def emit(self, record):
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelname

            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:  # ponytail: simplificado
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    # Aplica handler para logs de bibliotecas externas
    logging.basicConfig(
        handlers=[LoguruHandler()],
        level=logging.INFO,
    )

    logger.info("Logging configurado com sucesso")
    logger.info(f"Nível de log: {settings.log_level}")
    logger.info(f"Arquivo de log: {settings.log_file}")