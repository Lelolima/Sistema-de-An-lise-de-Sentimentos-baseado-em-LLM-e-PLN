"""Testes do módulo de modelos (VADER real, sem mocks)."""

import pytest

from src.sentiment_analysis.models import Sentiment, SentimentAnalyzer


@pytest.fixture(scope="module")
def analyzer():
    return SentimentAnalyzer(model="vader")


def test_positive(analyzer):
    r = analyzer.analyze("I love this product, it is excellent!")
    assert r.sentiment == Sentiment.POSITIVE
    assert 0 < r.confidence <= 1
    assert r.model_name == "vader"
    assert set(r.scores) == {"positive", "negative", "neutral", "compound"}


def test_negative(analyzer):
    assert analyzer.analyze("Terrible experience, I hate it.").sentiment == Sentiment.NEGATIVE


def test_neutral(analyzer):
    assert analyzer.analyze("The package arrived on Tuesday.").sentiment == Sentiment.NEUTRAL


def test_batch_preserves_order(analyzer):
    res = analyzer.analyze_batch(["great", "awful"])
    assert [r.sentiment for r in res] == [Sentiment.POSITIVE, Sentiment.NEGATIVE]


@pytest.mark.parametrize("bad", ["", "   "])
def test_empty_text_rejected(analyzer, bad):
    with pytest.raises(ValueError):
        analyzer.analyze(bad)
    with pytest.raises(ValueError):
        analyzer.analyze_batch(["ok", bad])


def test_unknown_model():
    with pytest.raises(ValueError):
        SentimentAnalyzer(model="nao-existe").analyze("x")


def test_available_models():
    assert {"vader", "bert"} <= set(SentimentAnalyzer.get_available_models())
