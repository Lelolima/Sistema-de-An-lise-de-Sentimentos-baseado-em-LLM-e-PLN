# Auditoria — Sistema de Análise de Sentimentos (LLM e PLN) — 2026-11-22

## Estado anterior

- Stack declarada: Python, FastAPI, Streamlit, transformers/torch, SQLAlchemy, Celery/Redis.
- **O núcleo não existia no repositório**: `src/sentiment_analysis/models/` (importado por API,
  dashboard e `main.py`) nunca foi commitado. Causa comprovada:
  `git check-ignore -v src/sentiment_analysis/models/base_model.py` → `.gitignore:48: models/`
  (a regra para pasta de pesos de modelo ignorava também o pacote Python).
- `python main.py` → `ModuleNotFoundError: No module named 'src.sentiment_analysis.models'`.
- `pytest` → 1 erro de coleta (`tests/api/test_api.py`); só os 7 testes de pré-processadores rodavam.
- Sem CI (só o "Dependency Graph" automático do GitHub).
- README anunciava VADER "PT-BR", GPT-4, Llama, coletores, Celery — nada disso implementado.

## Problemas

| # | Sev. | Problema | Evidência |
|---|---|---|---|
| 1 | P0 | Pacote `models` ausente → API, dashboard e demo não iniciam | erro acima; `.gitignore:48` |
| 2 | P0 | Dependência vulnerável sem correção: `python-jose 3.5.0` (PYSEC-2026-4298) e `ecdsa 0.19.2` (PYSEC-2026-1325) | `pip-audit` |
| 3 | P1 | Imports relativos errados nas rotas (`..models` → `sentiment_analysis.api.models`) | inspeção + ImportError |
| 4 | P1 | `api/__init__.py` importa `app` que não existia em `api/main.py` | `ImportError: cannot import name 'app'` |
| 5 | P1 | Dashboard: `NameError` (`exempolos`) e import relativo falha em `streamlit run` | inspeção |
| 6 | P1 | Sem CI | `gh run list` |
| 7 | P2 | `/history/clear` sempre retornava `entries_removed: 0` (contava após limpar) | teste `test_history_records_and_clear_counts` |
| 8 | P2 | Histórico nunca era alimentado pelas análises | idem |
| 9 | P2 | Modelo desconhecido / texto em branco no lote → HTTP 500 em vez de 400 | testes de regressão |
| 10 | P2 | `/health` retornava `"timestamp": "now"` (dado falso) | `test_health_has_real_timestamp` |
| 11 | P2 | `limit` negativo no histórico aceito | `test_history_negative_limit_rejected` |
| 12 | P2 | `requirements.txt` sem `python-jose` (usado) e `pyproject.toml` com config ruff obsoleta | inspeção |
| 13 | P2 | README não fiel à implementação | inspeção |

Segredos: busca por padrões de chave (`sk-`, `gsk_`, `hf_`, `ghp_`, `token/secret/password = "..."`)
no código atual e em `git log -p --all` → **nenhum segredo real**. `.env.example` só tem
placeholders. gitleaks não instalado nesta máquina.
Defaults inseguros (não são segredos vazados): `config.py` define `secret_key` e
`jwt_secret_key` com valores padrão públicos; CORS `allow_origins=["*"]` com credenciais.

## Mudanças

- `.gitignore`: `models/` → `/models/` (só a pasta de pesos na raiz).
- Novo `src/sentiment_analysis/models/` com o contrato usado pelo código existente:
  `Sentiment`, `SentimentResult`, `BaseSentimentModel`, `SentimentAnalyzer`
  (`analyze`, `analyze_batch`, `get_available_models`), `VaderModel` (`vaderSentiment`, real)
  e `BertModel` (opcional, `transformers`). **Reimplementação mínima** — o código original não está
  no histórico do git.
- Rotas: imports corrigidos, `ValueError` → 400, histórico alimentado, contagem do `clear` corrigida,
  `limit >= 0`; `app = api` em `api/main.py` (mantém os dois nomes públicos).
- `/health` com timestamp ISO real. Dashboard: typo e import corrigidos.
- `python-jose` → `PyJWT 2.15.0` em `api/middleware/auth.py` (mesma API pública:
  `create_access_token`, `verify_token`). Versões <2.15 do PyJWT também tinham avisos.
- `requirements-ci.txt` (subconjunto leve, versões testadas), `.github/workflows/ci.yml`
  (ruff + pytest + compileall, `contents: read`, actions por SHA).
- Testes novos: `tests/models/test_sentiment_analyzer.py`, `tests/api/test_auth.py`,
  regressões em `tests/api/test_api.py`.
- README com tabela "Estado real"; `.env.example` com `DEFAULT_MODEL=vader` e `BERT_MODEL_NAME`.

## Testes executados (local, Windows, Python 3.13, venv com `requirements-ci.txt`)

- Antes: `pytest` → 1 erro de coleta; `python main.py` → ModuleNotFoundError.
- Depois: `pytest -q` → **29 passed**.
- `ruff check --select E9,F63,F7,F82 src tests main.py` → ok.
- `pip-audit -r requirements-ci.txt` → No known vulnerabilities found.
- `uvicorn src.sentiment_analysis.api.main:api` → `/health` 200 com timestamp;
  `POST /api/v1/analyze/ {"text":"Excellent service!"}` → `positive`.
- `python main.py` → roda; os 6 exemplos em português: 1 `positive`, 5 `neutral`
  (limitação do léxico inglês do VADER, documentada).

## Não executado

- Modelo `bert`: exige `torch` + download do modelo (vários GB); não instalado aqui nem no CI.
- Dashboard Streamlit: não iniciado (streamlit fora do venv leve); só compilado.
- Docker / docker-compose: não executado (fora do escopo, sem deploy).

## Riscos residuais / decisões do dono

1. **O pacote `models` original se perdeu** (nunca commitado). Se o dono tiver os arquivos
   locais, eles devem substituir esta reimplementação. Por isso o PR fica **aberto** para revisão.
2. VADER não analisa português de verdade; para PT é preciso `bert` (ou um léxico PT) — decisão de produto.
3. `pip-audit -r requirements.txt` (dependências completas) apontou `oauthlib 3.3.1`
   (PYSEC-2026-4114 / CVE-2026-49272, corrigido em 4.0.1), transitiva de `tweepy`/Google API.
   Não fixei para não quebrar resolução de dependências não testadas.
4. Defaults de `secret_key`/`jwt_secret_key` e CORS aberto — definir antes de qualquer produção.
5. Scripts `force-push.bat`, `deploy-to-github.ps1`, `enviar-github.bat` fazem `git push --force`
   e `git add -A --force` (adicionaria `.env`). Não removi (funcionalidade do dono); recomendo apagar.
6. `requirements.txt` com faixas `>=` (não reprodutível); `pyproject.toml` com autor "Seu Nome" e URLs
   de repositório inexistente.
