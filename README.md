# My Cash Flow 💰

Sistema de controle financeiro composto por múltiplos microsserviços, orquestrados via Docker Compose.

## 📁 Estrutura do Projeto

```text
my-cash-flow/
├── docker-compose.yml    # Orquestrador de todas as aplicações
├── .env                  # Variáveis de ambiente compartilhadas
└── balance/              # Microsserviço de transações
    ├── src/
    ├── docs/
    ├── Dockerfile
    ├── app.py
    └── ...
```

---

# Balance - Transactions Microservice 💸

Microsserviço responsável pelo processamento de pagamentos e processamento de webhooks de múltiplos provedores (Mercado Pago, Santander, etc.), construído com **FastAPI** e seguindo os princípios da **Clean Architecture**.

## 🏗️ Arquitetura

O projeto foi refatorado para garantir manutenibilidade e escalabilidade, utilizando os seguintes padrões:

-   **Clean Architecture**: Separação clara entre Domínio, Aplicação, Infraestrutura e Apresentação.
-   **Strategy Pattern**: Implementado para lidar com diferentes provedores de webhooks de forma extensível.
-   **Dependency Injection**: Gestão desacoplada de dependências através da camada de infraestrutura.
-   **Repository Pattern**: Lógica de acesso a dados isolada do negócio.

### Estrutura de Pastas
```text
balance/src/
├── application/    # Casos de uso (Orquestração)
├── domain/         # Entidades de negócio e Interfaces (Coração)
├── infra/          # Implementações concretas (Banco, APIs Externas)
│   ├── core/       # Configurações e Logs
│   └── data/       # Repositórios, Migrations
└── presentation/   # Rotas API e ViewModels
```

## 🚀 Como Executar

O microsserviço pode ser executado de duas formas: manualmente (para desenvolvimento local rápido) ou via containers (Docker).

### Opção 1: Manual (Desenvolvimento)

#### Pré-requisitos
- Python 3.10+
- PostgreSQL
- Redis (para background tasks e cache)

#### Configuração
1. Clone o repositório.
2. Crie o seu arquivo `.env` na raiz baseado no exemplo:
   ```bash
   cp .env.example .env
   ```
3. Instale as dependências:
   ```bash
   cd balance
   pip install -r requirements.txt
   ```

#### Execução
```bash
# Sincronizar banco (Migrations)
cd balance
python -m src.infra.data.cli setup

# Rodar a API
python app.py
```

### Opção 2: Docker (Recomendado)

O projeto está configurado para rodar em conjunto com os outros serviços através do `docker-compose` na raiz do projeto.

```bash
# Na raiz do projeto (onde está o docker-compose.yml)
docker-compose up --build transactions_mcf
```

> [!IMPORTANT]
> **Automação**: Ao rodar via Docker, as **migrations** são executadas automaticamente pelo script [`entrypoint.sh`](./balance/entrypoint.sh) antes de iniciar a API.

---

## 🏗️ Banco de Dados (CLI)
Pode ser usado tanto localmente quanto dentro do container para manutenção:

```bash
# Apenas atualizar estrutura (Migrations)
cd balance
python -m src.infra.data.cli migrate

# Reverter alteração
python -m src.infra.data.cli rollback
```

## 🛡️ Segurança e Boas Práticas
-   **GitIgnore**: Proteção contra envio de segredos para o repositório.
-   **IA Protection**: Arquivo `.antigravityignore` para garantir privacidade contra leitura de segredos por IAs.
-   **Guia Técnico**: Documentação detalhada de regras de código disponível em [`docs/knowledge-base/technical-reference.md`](./balance/docs/knowledge-base/technical-reference.md).

## 🛠️ Tecnologias Principais
- **FastAPI**: Web Framework de alta performance.
- **SQLAlchemy/Alembic**: Gestão de banco de dados e versões.
- **Asyncpg**: Driver assíncrono para PostgreSQL.
- **Pydantic**: Validação de dados e modelos.
