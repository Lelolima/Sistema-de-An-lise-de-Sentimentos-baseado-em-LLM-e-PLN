"""Modelo léxico VADER (pacote ``vaderSentiment``).

Atenção: o léxico do VADER é em inglês. Textos em português só são pontuados
quando contêm palavras/emoticons presentes no léxico; o restante tende a "neutral".
"""

from .base_model import BaseSentimentModel, Sentiment, SentimentResult

POSITIVE_THRESHOLD = 0.05
NEGATIVE_THRESHOLD = -0.05


class VaderModel(BaseSentimentModel):
    """Baseline léxico, sem download de modelo nem GPU."""

    name = "vader"

    def __init__(self):
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

        self._analyzer = SentimentIntensityAnalyzer()

    def predict(self, text: str) -> SentimentResult:
        """Classifica pelo ``compound`` com os limiares oficiais do VADER (±0.05)."""
        raw = self._analyzer.polarity_scores(text)
        compound = raw["compound"]
        if compound >= POSITIVE_THRESHOLD:
            sentiment = Sentiment.POSITIVE
        elif compound <= NEGATIVE_THRESHOLD:
            sentiment = Sentiment.NEGATIVE
        else:
            sentiment = Sentiment.NEUTRAL
        scores = {"positive": raw["pos"], "negative": raw["neg"], "neutral": raw["neu"],
                  "compound": compound}
        confidence = abs(compound) if sentiment != Sentiment.NEUTRAL else raw["neu"]
        return SentimentResult(text=text, sentiment=sentiment, confidence=float(confidence),
                               scores=scores, model_name=self.name)
