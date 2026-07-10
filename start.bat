"""
Scripts de inicialização rápida.

Uso:
    start-api.bat     - Inicia a API FastAPI
    start-dashboard.bat - Inicia o dashboard Streamlit
    test.bat          - Executa os testes
"""

@echo off
echo ========================================
echo SISTEMA DE ANÁLISE DE SENTIMENTOS
echo ========================================
echo.

:: Verifica se o ambiente virtual existe
if not exist "venv" (
    echo [1/3] Criando ambiente virtual...
    python -m venv venv
)

:: Ativa o ambiente virtual
echo [2/3] Ativando ambiente virtual...
call venv\Scripts\activate.bat

:: Verifica dependências
echo [3/3] Verificando dependências...
pip show fastapi >nul 2>&1 || pip install -e .

echo.
echo ========================================
echo Escolha uma opção:
echo ========================================
echo 1. Iniciar API (FastAPI)
echo 2. Iniciar Dashboard (Streamlit)
echo 3. Executar testes
echo 4. Executar demo
echo 5. Sair
echo.

set /p opcao="Digite sua escolha (1-5): "

if "%opcao%"=="1" (
    echo Iniciando API em http://localhost:8000
    echo Documentação em http://localhost:8000/docs
    uvicorn src.sentiment_analysis.api.main:api --reload
) else if "%opcao%"=="2" (
    echo Iniciando Dashboard em http://localhost:8050
    streamlit run src/sentiment_analysis/dashboard/app.py
) else if "%opcao%"=="3" (
    echo Executando testes...
    pytest --cov=src -v
) else if "%opcao%"=="4" (
    echo Executando demo...
    python main.py
) else if "%opcao%"=="5" (
    echo Saindo...
    exit /b 0
) else (
    echo Opção inválida!
    pause
)