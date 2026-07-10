# Script de Inicialização e Push para o Repositório
# Executar: .\deploy-to-github.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SISTEMA DE ANÁLISE DE SENTIMENTOS" -ForegroundColor Cyan
Write-Host "Deploy para GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$repoUrl = "https://github.com/Lelolima/Sistema-de-An-lise-de-Sentimentos-baseado-em-LLM-e-PLN.git"
$commitMessage = "feat: estrutura completa do sistema de análise de sentimentos

- Estrutura de pastas organizada (src, tests, docs, assets)
- Módulo core: collectors, preprocessors, models
- API FastAPI com endpoints /analyze, /batch, /history
- Dashboard Streamlit
- Banco de dados SQLAlchemy
- 4 SVGs animados para documentação
- Documentação completa (README, CONTRIBUTING, CODE_OF_CONDUCT)
- Configuração Docker e docker-compose
- Testes unitários (pytest)
- Code review aplicado

Co-Authored-By: Claude <noreply@anthropic.com>"

Write-Host "Diretório: $(Get-Location)" -ForegroundColor Yellow
Write-Host "Repositório: $repoUrl" -ForegroundColor Yellow
Write-Host ""

# Verifica se é repo git, senão inicializa
if (-not (Test-Path ".git")) {
    Write-Host "[1/6] Inicializando repositório git..." -ForegroundColor Green
    git init
    Write-Host "      Repositório inicializado!" -ForegroundColor Green
} else {
    Write-Host "[1/6] Repositório git já existe" -ForegroundColor Green
}

# Configura usuario (se não configurado)
Write-Host "[2/6] Configurando git..." -ForegroundColor Green
git config user.name "Lelolima" 2>$null
git config user.email "lelolima@users.noreply.github.com" 2>$null

# Adiciona remote (remove se já existir)
Write-Host "[3/6] Configurando remote..." -ForegroundColor Green
git remote remove origin 2>$null
git remote add origin $repoUrl
Write-Host "      Remote configurado: $repoUrl" -ForegroundColor Green

# Adiciona todos os arquivos
Write-Host "[4/6] Adicionando arquivos..." -ForegroundColor Green
git add -A
Write-Host "      Arquivos adicionados ao staging!" -ForegroundColor Green

# Mostra resumo do que será enviado
Write-Host ""
Write-Host "Resumo dos arquivos:" -ForegroundColor Cyan
git status --short

Write-Host ""
Write-Host "[5/6] Criando commit..." -ForegroundColor Green
git commit -m $commitMessage

# Muda branch para main
Write-Host "      Mudando branch para main..." -ForegroundColor Green
git branch -M main 2>$null

# Faz push (force com --force-with-lease para segurança)
Write-Host "[6/6] Enviando para GitHub (force)..." -ForegroundColor Green
Write-Host "      ⚠️  Atenção: Forçando envio para substituir histórico existente" -ForegroundColor Yellow
Write-Host ""

# Tenta push com força
git push --force-with-lease origin main

# Verifica se成功了
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✅ DEPLOY CONCLUÍDO COM SUCESSO!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Repositório remoto:" -ForegroundColor Cyan
    Write-Host "https://github.com/Lelolima/Sistema-de-An-lise-de-Sentimentos-baseado-em-LLM-e-PLN" -ForegroundColor White
    Write-Host ""
    Write-Host "Próximos passos:" -ForegroundColor Cyan
    Write-Host "1. Acesse o repositório no GitHub" -ForegroundColor Gray
    Write-Host "2. Verifique se todos os arquivos foram enviados" -ForegroundColor Gray
    Write-Host "3. Atualize o nome do repositório se necessário" -ForegroundColor Gray
    Write-Host "4. Configure variáveis de ambiente no GitHub Secrets" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "❌ ERRO NO DEPLOY" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Possíveis causas:" -ForegroundColor Yellow
    Write-Host "- credenciais do GitHub não configuradas" -ForegroundColor Gray
    Write-Host "- repositório não existe ou está privado" -ForegroundColor Gray
    Write-Host "- permissões insuficientes" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Solução:" -ForegroundColor Cyan
    Write-Host "1. Verifique se está logado no GitHub:" -ForegroundColor Gray
    Write-Host "   gh auth status" -ForegroundColor White
    Write-Host ""
    Write-Host "2. Se necessário, autentique-se:" -ForegroundColor Gray
    Write-Host "   gh auth login" -ForegroundColor White
    Write-Host ""
    Write-Host "3. Tente novamente ou use push manual:" -ForegroundColor Gray
    Write-Host "   git push --force-with-lease origin main" -ForegroundColor White
}

Write-Host ""
Write-Host "Pressione qualquer tecla para sair..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")