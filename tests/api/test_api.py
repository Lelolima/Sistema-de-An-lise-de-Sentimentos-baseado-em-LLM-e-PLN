"""
Testes da API.
"""

import pytest
from fastapi.testclient import TestClient
from src.sentiment_analysis.api.main import api

client = TestClient(api)


class TestAPI:
    """Testes para a API FastAPI"""

    def test_root(self):
        """Testa endpoint raiz"""
        response = client.get("/")
        assert response.status_code == 200
        assert "name" in response.json()

    def test_health(self):
        """Testa health check"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_analyze_text(self):
        """Testa análise de texto"""
        response = client.post(
            "/api/v1/analyze/",
            json={"text": "Adorei o produto!", "model": "vader"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "sentiment" in data
        assert "confidence" in data

    def test_analyze_empty_text(self):
        """Testa análise de texto vazio"""
        response = client.post(
            "/api/v1/analyze/",
            json={"text": "", "model": "vader"},
        )
        assert response.status_code == 422  # Validation error

    def test_list_models(self):
        """Testa lista de modelos"""
        response = client.get("/api/v1/analyze/models")
        assert response.status_code == 200
        assert "models" in response.json()

    def test_batch_analyze(self):
        """Testa análise em lote"""
        response = client.post(
            "/api/v1/batch/",
            json={"texts": ["Bom!", "Ruim!"], "model": "vader"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "results" in data