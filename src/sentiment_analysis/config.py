"""
Configurações centrais do sistema.
Carrega variáveis de ambiente e define padrões.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Configurações do sistema carregadas do .env"""

    # ============================================
    # APIs de LLM
    # ============================================
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_api_base: str = Field(default="https://api.openai.com/v1", env="OPENAI_API_BASE")
    groq_api_key: Optional[str] = Field(default=None, env="GROQ_API_KEY")
    huggingface_api_key: Optional[str] = Field(default=None, env="HUGGINGFACE_API_KEY")

    # ============================================
    # Coleta de Dados
    # ============================================
    twitter_bearer_token: Optional[str] = Field(default=None, env="TWITTER_BEARER_TOKEN")
    twitter_api_key: Optional[str] = Field(default=None, env="TWITTER_API_KEY")
    twitter_api_secret: Optional[str] = Field(default=None, env="TWITTER_API_SECRET")
    google_api_key: Optional[str] = Field(default=None, env="GOOGLE_API_KEY")
    google_cx: Optional[str] = Field(default=None, env="GOOGLE_CX")

    # ============================================
    # Banco de Dados
    # ============================================
    database_url: str = Field(
        default="sqlite:///./sentimentos.db",
        env="DATABASE_URL"
    )

    # ============================================
    # Redis
    # ============================================
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")

    # ============================================
    # Configurações da API
    # ============================================
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    debug: bool = Field(default=False, env="DEBUG")
    secret_key: str = Field(default="secret-key-change-in-production", env="SECRET_KEY")

    # JWT
    jwt_secret_key: str = Field(default="jwt-secret-key", env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # ============================================
    # Configurações de Modelos
    # ============================================
    default_model: str = Field(default="bertabaporu-dimensional", env="DEFAULT_MODEL")
    use_model_cache: bool = Field(default=True, env="USE_MODEL_CACHE")
    model_cache_dir: str = Field(default="./models/cache", env="MODEL_CACHE_DIR")
    use_quantization: bool = Field(default=False, env="USE_QUANTIZATION")

    # ============================================
    # Processamento
    # ============================================
    max_batch_size: int = Field(default=100, env="MAX_BATCH_SIZE")
    max_text_length: int = Field(default=512, env="MAX_TEXT_LENGTH")
    enable_async_processing: bool = Field(default=True, env="ENABLE_ASYNC_PROCESSING")

    # ============================================
    # Logging
    # ============================================
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="./logs/sistema.log", env="LOG_FILE")

    # ============================================
    # Dashboard
    # ============================================
    dashboard_host: str = Field(default="0.0.0.0", env="DASHBOARD_HOST")
    dashboard_port: int = Field(default=8050, env="DASHBOARD_PORT")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore",
    }


# Instância global das configurações
settings = Settings()


def get_settings() -> Settings:
    """Retorna as configurações do sistema (útil para injeção de dependência)"""
    return settings