# Documentação do Sistema de Análise de Sentimentos

A documentação completa está disponível no README.md. Este diretório contém documentação adicional.

## Estrutura de Diretórios

```
src/sentiment_analysis/
├── collectors/      # Coleta de dados (Twitter, Google, arquivos)
├── preprocessors/   # Pré-processamento (limpeza, tokenização, normalização)
├── models/          # Modelos de análise (VADER, BERT, LLM)
├── api/             # API FastAPI
├── dashboard/       # Dashboard Streamlit
├── database/        # Banco de dados e modelos ORM
└── utils/           # Utilitários (cache, métricas)
```

## Guia de Início Rápido

### 1. Instalação

```bash
pip install -e ".[dev]"
```

### 2. Configuração

```bash
cp .env.example .env
# Edite .env com suas chaves de API
```

### 3. Uso Básico

```python
from sentiment_analysis.models import SentimentAnalyzer

analyzer = SentimentAnalyzer(model="vader")
result = analyzer.analyze("Adorei o produto!")
print(result.sentiment, result.confidence)
```

### 4. Executar API

```bash
uvicorn src.sentiment_analysis.api.main:api --reload
```

### 5. Executar Dashboard

```bash
streamlit run src/sentiment_analysis/dashboard/app.py
```

## Arquitetura

O sistema segue uma arquitetura modular:

1. **Collectors**: Coletam dados de várias fontes
2. **Preprocessors**: Limpam e normalizam o texto
3. **Models**: Analisam o sentimento
4. **API**: Expõe endpoints REST
5. **Dashboard**: Interface visual

## Contribuição

Veja o arquivo CONTRIBUTING.md (em breve) para diretrizes de contribuição.