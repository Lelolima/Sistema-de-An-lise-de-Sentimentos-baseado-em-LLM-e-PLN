@echo off
setlocal EnableDelayedExpansion

echo ========================================
echo ENVIAR PARA GITHUB - FORCE PUSH
echo ========================================
echo.

set REPO_URL=https://github.com/Lelolima/Sistema-de-An-lise-de-Sentimentos-baseado-em-LLM-e-PLN.git

cd /d "%~dp0"

echo Diretório: %CD%
echo.

:: Verifica se git está instalado
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Git não instalado!
    echo Baixe em: https://git-scm.com/downloads
    pause
    exit /b 1
)

:: Inicializa repo se não existir
if not exist ".git" (
    echo [1/7] Inicializando repositório git...
    git init
    echo.
) else (
    echo [1/7] Repositório git já existe
)

:: Configura usuário
echo [2/7] Configurando usuário git...
git config user.name "Lelolima"
git config user.email "lelolima@users.noreply.github.com"

:: Remove e adiciona remote
echo [3/7] Configurando remote...
git remote remove origin 2>nul
git remote add origin %REPO_URL%
echo Remote: %REPO_URL%
echo.

:: Adiciona arquivos
echo [4/7] Adicionando arquivos ao staging...
git add -A
echo.

:: Mostra resumo
echo Arquivos a serem enviados:
echo ----------------------------------------
git status --short
echo ----------------------------------------
echo.

:: Cria commit
echo [5/7] Criando commit...
git commit -m "feat: estrutura completa do sistema de analise de sentimentos

- Estrutura de pastas organizada (src, tests, docs, assets)
- Modulos: collectors, preprocessors, models
- API FastAPI com endpoints /analyze, /batch, /history
- Dashboard Streamlit
- 4 SVGs animados para documentacao
- Code review aplicado

Co-Authored-By: Claude <noreply@anthropic.com>"
echo.

:: Muda para main
echo [6/7] Renomeando branch para main...
git branch -M main 2>nul

:: Force push
echo [7/7] Enviando para GitHub (FORCE PUSH)...
echo.
echo ========================================
echo ATENCAO: Forcando envio!
echo ========================================
echo.

git push --force-with-lease origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  ✅ ENVIO CONCLUÍDO COM SUCESSO!
    echo ========================================
    echo.
    echo Repositório:
    echo %REPO_URL%
    echo.
) else (
    echo.
    echo ========================================
    echo  ❌ ERRO NO ENVIO
    echo ========================================
    echo.
    echo Possiveis causas:
    echo - Credenciais do GitHub não configuradas
    echo - Repositório não existe ou está privado
    echo - Permissões insuficientes
    echo.
    echo Solucao:
    echo 1. gh auth login
    echo 2. ou git push --force-with-lease origin main
    echo.
)

pause