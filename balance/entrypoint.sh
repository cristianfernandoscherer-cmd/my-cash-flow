#!/bin/bash
set -e

echo "⏳ Aguardando banco de dados ficar pronto..."

# Aguarda o banco ficar acessível
python -c "
import time
import psycopg2
import os

db_url = os.getenv('DATABASE_URL')
if not db_url:
    print('❌ DATABASE_URL não configurada')
    exit(1)

print(f'📦 Conectando ao banco...')
for i in range(30):
    try:
        conn = psycopg2.connect(db_url)
        conn.close()
        print('✅ Banco de dados pronto!')
        break
    except Exception as e:
        print(f'⏳ Aguardando banco... ({i+1}/30)')
        time.sleep(2)
"

echo "🛠️  Rodando migrations..."
python -m src.infra.data.cli migrate

echo "🚀 Iniciando aplicação..."
exec "$@"