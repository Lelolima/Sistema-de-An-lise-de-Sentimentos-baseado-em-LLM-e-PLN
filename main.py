"""
Script inicial para teste rápido do sistema.

Uso: python main.py
"""

from src.sentiment_analysis.models import SentimentAnalyzer
from src.sentiment_analysis.preprocessors import TextCleaner


def main():
    """Demo do sistema de análise de sentimentos"""
    print("=" * 60)
    print("SISTEMA DE ANÁLISE DE SENTIMENTOS - DEMO")
    print("=" * 60)

    # Inicializa componentes
    cleaner = TextCleaner()
    analyzer = SentimentAnalyzer(model="vader")

    # Textos de exemplo
    exemplos = [
        "Este produto é excelente! Super recomendo.",
        "Péssima experiência, não comprem.",
        "O produto chegou dentro do prazo, nada demais.",
        "Amei! Melhor compra que já fiz.",
        "Decepção total, esperava muito mais.",
        "Mais ou menos, dentro do esperado.",
    ]

    print("\n📊 Analisando exemplos:\n")

    for texto in exemplos:
        # Limpa o texto
        texto_limpo = cleaner.clean(texto)

        # Analisa
        resultado = analyzer.analyze(texto_limpo)

        # Exibe resultado
        emoji = {"positive": "😊", "negative": "😞", "neutral": "😐"}
        print(f"Texto: {texto[:50]}...")
        print(f"  → Sentimento: {emoji.get(resultado.sentiment.value, '?')} {resultado.sentiment.value}")
        print(f"  → Confiança: {resultado.confidence:.1%}")
        print()

    print("=" * 60)
    print("Demo concluída!")
    print("Para iniciar a API: uvicorn src.sentiment_analysis.api.main:api --reload")
    print("Para o dashboard: streamlit run src/sentiment_analysis/dashboard/app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()