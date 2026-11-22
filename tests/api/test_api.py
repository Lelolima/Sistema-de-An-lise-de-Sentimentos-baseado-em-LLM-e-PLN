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

class TestAPIRegressions:
    """Regressões encontradas na auditoria de 2026-11-22."""

    def setup_method(self):
        client.post("/api/v1/history/clear")

    def test_unknown_model_returns_400(self):
        r = client.post("/api/v1/analyze/", json={"text": "good", "model": "nao-existe"})
        assert r.status_code == 400

    def test_blank_text_in_batch_returns_400(self):
        r = client.post("/api/v1/batch/", json={"texts": ["good", "  "]})
        assert r.status_code == 400

    def test_history_records_and_clear_counts(self):
        client.post("/api/v1/analyze/", json={"text": "I love it"})
        client.post("/api/v1/batch/", json={"texts": ["great", "awful"]})
        h = client.get("/api/v1/history/").json()
        assert h["total"] == 3
        stats = client.get("/api/v1/history/stats").json()
        assert stats["positive"] == 2 and stats["negative"] == 1
        r = client.post("/api/v1/history/clear").json()
        assert r["entries_removed"] == 3

    def test_history_negative_limit_rejected(self):
        assert client.get("/api/v1/history/?limit=-1").status_code == 422

    def test_health_has_real_timestamp(self):
        from datetime import datetime

        ts = client.get("/health").json()["timestamp"]
        datetime.fromisoformat(ts)
