#!/bin/bash
set -e

echo "📁 Criando diretório de logs..."
mkdir -p /app/logs

echo "⌛ Aguardando banco de dados..."

# Executa as migrations
echo "🛠️  Rodando migrations..."
python -m src.infra.data.cli migrate

# Inicia o comando passado pelo CMD
echo "🚀 Iniciando processo..."
exec "$@"