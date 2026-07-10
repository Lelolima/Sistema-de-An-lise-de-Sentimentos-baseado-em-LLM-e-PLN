# Sistema de Análise de Sentimentos com LLM e PLN

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Um sistema completo de análise de sentimentos combinando **Large Language Models (LLMs)** e **Processamento de Linguagem Natural (PLN)** para análise de texto em português e múltiplos idiomas.

---

## 🎯 Visão Geral do Sistema

![System Overview](docs/assets/system-overview.svg)

---

## 🚀 Funcionalidades

- **Análise de Sentimentos Multi-Modelo**: Combine LLMs (GPT, Llama, Mixtral) com modelos tradicionais (BERT, VADER)
- **Suporte Multilíngue**: Foco em português brasileiro com suporte para inglês e espanhol
- **Coleta de Dados**: Integração com Twitter/X, Google Reviews, e outras fontes
- **API RESTful**: FastAPI com endpoints para análise em tempo real e em lote
- **Dashboard Interativo**: Visualizações com Plotly/Dash e Streamlit
- **Processamento Assíncrono**: Celery + Redis para grandes volumes de dados
- **Cache Inteligente**: Redis/SQLite para resultados frequentes

---

## 📋 Arquitetura

![Architecture Diagram](docs/assets/architecture-diagram.svg)

### Fluxo de Análise

![Analysis Flow](docs/assets/analysis-flow.svg)

### Dashboard em Tempo Real

![Dashboard](docs/assets/realtime-dashboard.svg)

---

## 📁 Estrutura do Projeto

```
sistema-analise-sentimentos-pln/
├── src/
│   └── sentiment_analysis/
│       ├── __init__.py              # Pacote principal
│       ├── config.py                # Configurações centrais
│       ├── logging_config.py        # Configuração de logs
│       │
│       ├── collectors/              # Coleta de dados
│       │   ├── base_collector.py    # Interface base
│       │   └── file_collector.py    # Coletor de arquivos
│       │
│       ├── preprocessors/           # Pré-processamento
│       │   ├── text_cleaner.py      # Limpeza de texto
│       │   ├── tokenizer.py         # Tokenização
│       │   └── normalizer.py        # Normalização
│       │
│       ├── models/                  # Modelos de análise
│       │   ├── base_model.py        # Interface base
│       │   ├── vader_model.py       # VADER (baseline)
│       │   ├── bert_model.py        # BERT/HuggingFace
│       │   └── sentiment_analyzer.py # Fachada unificada
│       │
│       ├── api/                     # API FastAPI
│       │   ├── main.py              # App principal
│       │   ├── routes/              # Rotas da API
│       │   ├── schemas/             # Pydantic schemas
│       │   └── middleware/          # Middleware (auth)
│       │
│       ├── dashboard/               # Dashboard
│       │   └── app.py               # Streamlit app
│       │
│       ├── database/                # Banco de dados
│       │   ├── connection.py        # SQLAlchemy
│       │   └── models.py            # ORM models
│       │
│       └── utils/                   # Utilitários
│           └── cache.py             # Cache system
│
├── tests/
│   ├── api/
│   ├── models/
│   └── preprocessors/
│
├── docs/
│   └── assets/                      # SVGs e imagens
│
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.9 ou superior
- pip ou poetry
- (Opcional) PostgreSQL para produção
- (Opcional) Redis para cache

### Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/Lelolima/sistema-analise-sentimentos-llm-pln.git
cd sistema-analise-sentimentos-llm-pln

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Instale as dependências
pip install -e ".[dev]"

# Configure as variáveis de ambiente
cp .env.example .env
# Edite .env com suas chaves de API
```

---

## ⚙️ Configuração

Edite o arquivo `.env` com suas credenciais:

```bash
# APIs de LLM
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...
HUGGINGFACE_API_KEY=hf_...

# Banco de Dados
DATABASE_URL=postgresql://user:pass@localhost:5432/sentimentos_db

# Redis
REDIS_URL=redis://localhost:6379/0
```

---

## 📖 Uso

### Análise Simples de Texto

```python
from sentiment_analysis.models import SentimentAnalyzer

analyzer = SentimentAnalyzer(model="vader")
resultado = analyzer.analyze("Este produto é excelente! Adorei a qualidade.")

print(f"Sentimento: {resultado.sentiment}")
print(f"Confiança: {resultado.confidence:.2%}")
```

### Análise em Lote

```python
analyzer = SentimentAnalyzer(model="vader")

textos = [
    "Adorei o atendimento!",
    "Péssimo produto, não recomendo.",
    "Mais ou menos, dentro do esperado."
]

resultados = analyzer.analyze_batch(textos)
for r in resultados:
    print(f"{r.text[:30]}... -> {r.sentiment}")
```

### Via API

```bash
# Iniciar a API
uvicorn src.sentiment_analysis.api.main:api --reload

# Requisição
curl -X POST "http://localhost:8000/api/v1/analyze" \
     -H "Content-Type: application/json" \
     -d '{"text": "Produto excelente, recomendo!"}'
```

### Dashboard

```bash
# Iniciar o dashboard
streamlit run src/sentiment_analysis/dashboard/app.py
```

---

## 🔧 Modelos Suportados

| Modelo | Tipo | Idioma | Uso |
|--------|------|--------|-----|
| `vader` | Léxico | PT-BR | Padrão/Baseline |
| `bert` | Transformer | PT-BR | Alta precisão |
| `gpt-4` | LLM | Multi | Via API |
| `llama-3` | LLM | Multi | Local ou Groq |

---

## 📊 Dashboard

O dashboard inclui:

- 📈 Distribuição de sentimentos (positivo, neutro, negativo)
- 📅 Evolução temporal da polaridade
- ☁️ Word cloud dos termos mais frequentes
- 📊 Análise por categoria/tópico
- 📥 Exportação de relatórios (PDF, Excel)

---

## 🧪 Testes

```bash
# Rodar todos os testes
pytest

# Com coverage
pytest --cov=src

# Testes específicos
pytest tests/models/test_sentiment_analyzer.py
```

---

## 📦 Deploy com Docker

```bash
# Build da imagem
docker build -t sentiment-analysis .

# Rodar com docker-compose
docker-compose up -d

# Serviços:
# - API: http://localhost:8000
# - Dashboard: http://localhost:8050
# - PostgreSQL: localhost:5432
# - Redis: localhost:6379
```

---

## 🗺️ Roadmap

| Fase | Status | Descrição |
|------|--------|-----------|
| ✅ Fase 1 | Completa | Estrutura básica, config, docs |
| 🔄 Fase 2 | Em andamento | Core pipeline (preprocess + models) |
| 📋 Fase 3 | Planejada | API completa + Dashboard |
| 📋 Fase 4 | Planejada | Collectors + Otimização |
| 📋 Fase 5 | Planejada | Features avançadas |

---

## 🤝 Contribuição

Contribuições são bem-vindas!

1. Fork o projeto
2. Crie uma feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Licença MIT. Veja [LICENSE](LICENSE) para detalhes.

---

## 🙏 Agradecimentos

- [Hugging Face](https://huggingface.co/) - Transformers
- [spaCy](https://spacy.io/) - PLN
- [FastAPI](https://fastapi.tiangolo.com/) - API
- [Plotly](https://plotly.com/) - Visualizações
- [Streamlit](https://streamlit.io/) - Dashboard

---

## 📞 Contato

- GitHub: [@Lelolima](https://github.com/Lelolima)
- Issues: [GitHub Issues](https://github.com/Lelolima/sistema-analise-sentimentos-llm-pln/issues)

---

**Nota**: Projeto em desenvolvimento ativo. Algumas funcionalidades podem estar em estado experimental.