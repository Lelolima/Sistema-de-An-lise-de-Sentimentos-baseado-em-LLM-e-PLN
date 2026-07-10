"""
Testes do pré-processador de texto.
"""

import pytest
from src.sentiment_analysis.preprocessors import TextCleaner, Normalizer


class TestTextCleaner:
    """Testes para o limpador de texto"""

    def test_lowercase(self):
        """Testa conversão para minúsculas"""
        cleaner = TextCleaner(lowercase=True)
        assert cleaner.clean("TEXTO") == "texto"

    def test_remove_urls(self):
        """Testa remoção de URLs"""
        cleaner = TextCleaner(remove_urls=True)
        assert "http" not in cleaner.clean("Visite https://exemplo.com")

    def test_remove_mentions(self):
        """Testa remoção de menções"""
        cleaner = TextCleaner(remove_mentions=True)
        assert "@" not in cleaner.clean("Olá @usuario!")

    def test_clean_batch(self):
        """Testa limpeza em lote"""
        cleaner = TextCleaner()
        textos = ["TEXTO!", "Outro Texto", "Mais Um"]

        results = cleaner.clean_batch(textos)

        assert len(results) == 3
        assert all(t.islower() for t in results)


class TestNormalizer:
    """Testes para o normalizador"""

    def test_remove_accents(self):
        """Testa remoção de acentos"""
        normalizer = Normalizer(remove_accents=True)
        assert normalizer.normalize("ação") == "acao"

    def test_repeated_chars(self):
        """Testa normalização de caracteres repetidos"""
        normalizer = Normalizer(normalize_repeated_chars=True)
        result = normalizer.normalize("gooooosto")
        assert "oooo" not in result

    def test_normalize_batch(self):
        """Testa normalização em lote"""
        normalizer = Normalizer()
        textos = ["ação", "maçã", "café"]

        results = normalizer.normalize_batch(textos)

        assert results == ["acao", "maca", "cafe"]