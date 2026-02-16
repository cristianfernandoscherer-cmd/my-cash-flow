#!/bin/bash
set -e

# Aguarda o banco de dados estar pronto (opcional, já tratado pelo depends_on healthcheck no compose)
echo "⌛ Aguardando banco de dados..."

# Executa as migrations
echo "🛠️  Rodando migrations..."
python -m src.infra.data.cli migrate

# Inicia o comando passado pelo CMD do Dockerfile (ou argumentos manuais)
echo "🚀 Iniciando processo..."
exec "$@"
