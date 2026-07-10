"""
Autenticação JWT para a API.

ponytail: Implementação básica - expandir para produção.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt

from ...config import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria token de acesso JWT.

    Args:
        data: Dados a codificar no token
        expires_delta: Duração do token

    Returns:
        str: Token JWT
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def verify_token(token: str) -> Optional[dict]:
    """
    Verifica e decodifica token JWT.

    Args:
        token: Token JWT

    Returns:
        dict: Dados do token ou None se inválido
    """
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        return None