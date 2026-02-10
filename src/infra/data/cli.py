import asyncio
import argparse
import sys
import os
from alembic.config import Config
from alembic import command

# Adiciona o diretório atual ao sys.path para garantir que o Alembic encontre o app
sys.path.insert(0, os.getcwd())

from .database import db

def get_alembic_config():
    """Configura o objeto de configuração do Alembic"""
    config = Config("alembic.ini")
    return config

def run_migrate():
    """Executa as migrations para a versão mais recente"""
    print("🛠️  Executando migrations...")
    alembic_cfg = get_alembic_config()
    command.upgrade(alembic_cfg, "head")
    print("✅ Migrations aplicadas!")

def run_rollback():
    """Volta uma versão do banco de dados"""
    print("⏪ Revertendo última migration...")
    alembic_cfg = get_alembic_config()
    command.downgrade(alembic_cfg, "-1")
    print("✅ Rollback concluído!")

async def run_setup():
    """Executa migrations"""
    print("🚀 Iniciando setup completo do banco...")
    run_migrate()
    print("✨ Setup finalizado com sucesso!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Database Management CLI")
    parser.add_argument(
        "command", 
        choices=["migrate", "rollback", "seed", "setup"], 
        help="Command to run"
    )
    
    args = parser.parse_args()
    
    if args.command == "migrate":
        run_migrate()
    elif args.command == "rollback":
        run_rollback()
    elif args.command == "setup":
        asyncio.run(run_setup())
