"""
Dashboard Streamlit para visualização de análises.
"""

import streamlit as st
from datetime import datetime
from typing import List, Dict

from ..models.sentiment_analyzer import SentimentAnalyzer
from ..models.base_model import Sentiment


def create_dashboard():
    """
    Cria e executa o dashboard Streamlit.

    Configura a página e os componentes principais.
    """
    st.set_page_config(
        page_title="Análise de Sentimentos - Dashboard",
        page_icon="📊",
        layout="wide",
    )

    st.title("📊 Dashboard de Análise de Sentimentos")
    st.markdown("---")

    # Sidebar com configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        model = st.selectbox(
            "Modelo",
            options=["vader", "bert"],
            help="Escolha o modelo para análise",
        )
        st.markdown("---")
        st.markdown("**Sobre**")
        st.markdown("Sistema de Análise de Sentimentos")
        st.markdown(f"Versão: 0.1.0")

    # Área principal
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📝 Nova Análise")
        text = st.text_area(
            "Digite o texto para análise",
            height=150,
            placeholder="Ex: Adorei o produto! Qualidade excelente e entrega rápida.",
        )

    with col2:
        st.subheader("📈 Resultado")
        if st.button("Analisar", type="primary"):
            if text:
                with st.spinner("Analisando..."):
                    try:
                        analyzer = SentimentAnalyzer(model=model)
                        result = analyzer.analyze(text)

                        # Exibe resultado
                        if result.sentiment == Sentiment.POSITIVE:
                            st.metric("Sentimento", "Positivo 😊")
                        elif result.sentiment == Sentiment.NEGATIVE:
                            st.metric("Sentimento", "Negativo 😞")
                        else:
                            st.metric("Sentimento", "Neutro 😐")

                        st.metric("Confiança", f"{result.confidence:.1%}")

                        # Scores detalhados
                        if result.scores:
                            st.json(result.scores)
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")
            else:
                st.warning("Digite um texto para analisar")

    # Seção de exemplos
    st.markdown("---")
    st.subheader("📚 Exemplos Rápidos")

    exemplos = [
        "Este produto é excelente! Super recomendo.",
        "Péssima experiência, não comprem.",
        "O produto chegou dentro do prazo, nada demais.",
        "Amei! Melhor compra que já fiz.",
        "Decepção total, esperava muito mais.",
    ]

    cols = st.columns(5)
    for i, exemplo in enumerate(exempolos):
        with cols[i]:
            if st.button(f"Ex {i+1}", key=f"ex{i}"):
                st.session_state["exemplo_texto"] = exemplo

    if "exemplo_texto" in st.session_state:
        st.info(f"Selecionado: {st.session_state['exemplo_texto']}")

    # Rodapé
    st.markdown("---")
    st.markdown(
        "🔗 [Código Fonte](https://github.com/Lelolima/sistema-analise-sentimentos-llm-pln)"
    )


def run():
    """Executa o dashboard"""
    create_dashboard()


if __name__ == "__main__":
    run()