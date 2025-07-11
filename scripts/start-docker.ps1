#!/usr/bin/env pwsh
# Script para executar o Taskaio API com Docker

Write-Host "🚀 Iniciando Taskaio API com Docker..." -ForegroundColor Green

# Verificar se Docker está instalado
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker não está instalado ou não está no PATH" -ForegroundColor Red
    Write-Host "   Instale o Docker Desktop: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Verificar se Docker está rodando
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Docker não está rodando" -ForegroundColor Red
    Write-Host "   Inicie o Docker Desktop e tente novamente" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Docker está rodando" -ForegroundColor Green

# Construir e executar os containers
Write-Host "🔨 Construindo e executando containers..." -ForegroundColor Blue
docker-compose up -d --build

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Containers executados com sucesso!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Informações dos serviços:" -ForegroundColor Cyan
    Write-Host "   • API: http://localhost:8000" -ForegroundColor White
    Write-Host "   • Documentação: http://localhost:8000/docs" -ForegroundColor White
    Write-Host "   • MongoDB: mongodb://localhost:27017" -ForegroundColor White
    Write-Host ""
    Write-Host "🔍 Testando a API..." -ForegroundColor Blue
    
    # Aguardar um pouco para a API iniciar
    Start-Sleep -Seconds 5
    
    # Testar a API
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000" -Method Get -TimeoutSec 10
        Write-Host "✅ API está respondendo: $($response.message)" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  API ainda está iniciando... Tente acessar em alguns segundos" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "📝 Comandos úteis:" -ForegroundColor Cyan
    Write-Host "   • Ver logs: npm run docker:logs" -ForegroundColor White
    Write-Host "   • Parar: npm run docker:down" -ForegroundColor White
    Write-Host "   • Reiniciar: npm run docker:restart" -ForegroundColor White
    Write-Host ""
    Write-Host "🎉 Taskaio API está pronta para uso!" -ForegroundColor Green
} else {
    Write-Host "❌ Erro ao executar containers" -ForegroundColor Red
    Write-Host "   Verifique os logs para mais detalhes" -ForegroundColor Yellow
    exit 1
}
