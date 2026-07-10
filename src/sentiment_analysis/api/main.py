"""
Aplicação principal da API FastAPI.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from ..config import settings
from ..logging_config import setup_logging
from .routes import analyze, batch, history

# Configura logging
setup_logging()

# Cria aplicação FastAPI
api = FastAPI(
    title="Sistema de Análise de Sentimentos - API",
    description="API RESTful para análise de sentimentos usando LLM e PLN",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configura CORS
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ponytail: aberto para desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.on_event("startup")
async def startup_event():
    """Executado na inicialização da API"""
    logger.info("Iniciando API de Análise de Sentimentos")
    logger.info(f"Debug: {settings.debug}")
    logger.info(f"Modelo padrão: {settings.default_model}")


@api.on_event("shutdown")
async def shutdown_event():
    """Executado no desligamento da API"""
    logger.info("API de Análise de Sentimentos desligada")


@api.get("/")
async def root():
    """Endpoint raiz - informações da API"""
    return {
        "name": "Sistema de Análise de Sentimentos API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
    }


@api.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "now"}


# Registra rotas
api.include_router(analyze.router, prefix="/api/v1/analyze", tags=["Análise"])
api.include_router(batch.router, prefix="/api/v1/batch", tags=["Batch"])
api.include_router(history.router, prefix="/api/v1/history", tags=["Histórico"])