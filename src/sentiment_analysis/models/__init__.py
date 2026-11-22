"""Modelos de análise de sentimentos."""

from .base_model import BaseSentimentModel, Sentiment, SentimentResult
from .sentiment_analyzer import SentimentAnalyzer

__all__ = ["BaseSentimentModel", "Sentiment", "SentimentResult", "SentimentAnalyzer"]
