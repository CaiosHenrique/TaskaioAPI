#!/bin/bash
# Script para executar o Taskaio API com Docker

echo "🚀 Iniciando Taskaio API com Docker..."

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado ou não está no PATH"
    echo "   Instale o Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Verificar se Docker está rodando
if ! docker info &> /dev/null; then
    echo "❌ Docker não está rodando"
    echo "   Inicie o Docker e tente novamente"
    exit 1
fi

echo "✅ Docker está rodando"

# Construir e executar os containers
echo "🔨 Construindo e executando containers..."
docker-compose up -d --build

if [ $? -eq 0 ]; then
    echo "✅ Containers executados com sucesso!"
    echo ""
    echo "📋 Informações dos serviços:"
    echo "   • API: http://localhost:8000"
    echo "   • Documentação: http://localhost:8000/docs"
    echo "   • MongoDB: mongodb://localhost:27017"
    echo ""
    echo "🔍 Testando a API..."
    
    # Aguardar um pouco para a API iniciar
    sleep 5
    
    # Testar a API
    if curl -s http://localhost:8000 > /dev/null; then
        response=$(curl -s http://localhost:8000 | grep -o '"message":"[^"]*"' | cut -d'"' -f4)
        echo "✅ API está respondendo: $response"
    else
        echo "⚠️  API ainda está iniciando... Tente acessar em alguns segundos"
    fi
    
    echo ""
    echo "📝 Comandos úteis:"
    echo "   • Ver logs: npm run docker:logs"
    echo "   • Parar: npm run docker:down"
    echo "   • Reiniciar: npm run docker:restart"
    echo ""
    echo "🎉 Taskaio API está pronta para uso!"
else
    echo "❌ Erro ao executar containers"
    echo "   Verifique os logs para mais detalhes"
    exit 1
fi
