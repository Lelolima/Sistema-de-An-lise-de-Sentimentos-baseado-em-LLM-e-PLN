"""
Conexão e configuração do banco de dados.
"""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from loguru import logger

from ..config import settings


class DatabaseConfig:
    """Configuração do banco de dados"""

    def __init__(self, url: str = None):
        self.url = url or settings.database_url
        self._engine = None
        self._session_maker = None

    @property
    def engine(self):
        """Retorna ou cria o engine"""
        if self._engine is None:
            self._engine = create_engine(
                self.url,
                echo=settings.debug,
                pool_pre_ping=True,  # ponytail: detecta conexões mortas
            )
            logger.info("Conexão com banco de dados estabelecida")
        return self._engine

    @property
    def session_maker(self):
        """Retorna ou cria o session maker"""
        if self._session_maker is None:
            self._session_maker = sessionmaker(
                bind=self.engine, autocommit=False, autoflush=False
            )
        return self._session_maker

    def create_tables(self):
        """Cria as tabelas no banco de dados"""
        from .models import Base

        Base.metadata.create_all(bind=self.engine)
        logger.info("Tabelas criadas com sucesso")


# Instância global
db_config = DatabaseConfig()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency para obter sessão do banco de dados.

    Uso:
        @router.get("/")
        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = db_config.session_maker()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()