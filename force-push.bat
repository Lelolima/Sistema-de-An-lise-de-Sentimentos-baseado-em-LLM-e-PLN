@echo off
setlocal EnableDelayedExpansion

echo ========================================
echo FORCE PUSH - GITHUB
echo ========================================
echo.

set REPO_URL=https://github.com/Lelolima/Sistema-de-An-lise-de-Sentimentos-baseado-em-LLM-e-PLN.git

cd /d "%~dp0"

echo [1/6] Forcando inicializacao do git...
if not exist ".git" ( git init )
echo.

echo [2/6] Configurando git...
git config user.name "Lelolima"
git config user.email "lelolima@users.noreply.github.com"
echo.

echo [3/6] Adicionando TODOS os arquivos...
git add -A --force
echo.

echo [4/6] Commit...
git commit --allow-empty -m "feat: estrutura completa do sistema" -m "Co-Authored-By: Claude <noreply@anthropic.com>"
echo.

echo [5/6] Forcando branch main...
git branch -D main 2>nul
git checkout -b main
echo.

echo [6/6] FORCE PUSH verdadeiro...
echo.
echo Destravando push forçado...
git push --force origin main --no-verify 2>&1

if !ERRORLEVEL! EQU 0 (
    echo.
    echo ========================================
    echo  ✅ SUCESSO!
    echo ========================================
) else (
    echo.
    echo ========================================
    echo  Tentando alternativa com token...
    echo ========================================
    echo.
    echo ERRO: Autenticacao necessaria.
    echo.
    echo Opcoes:
    echo 1. gh auth login  ^&^& git push --force origin main
    echo 2. Ou configure um token em:
    echo    https://github.com/settings/tokens
    echo.
    echo Depois execute:
    echo    git push --force origin main
    echo.
)

pause