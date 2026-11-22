"""Testes do utilitário JWT."""

from datetime import timedelta

from src.sentiment_analysis.api.middleware.auth import create_access_token, verify_token


def test_roundtrip():
    tok = create_access_token({"sub": "alice"})
    assert verify_token(tok)["sub"] == "alice"


def test_expired_token_rejected():
    tok = create_access_token({"sub": "a"}, expires_delta=timedelta(seconds=-1))
    assert verify_token(tok) is None


def test_tampered_token_rejected():
    tok = create_access_token({"sub": "a"})
    assert verify_token(tok[:-2] + ("AA" if not tok.endswith("AA") else "BB")) is None
