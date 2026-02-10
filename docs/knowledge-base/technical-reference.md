# 🧠 Guia de Referência Técnica - Transactions Microservice

Este documento serve como a "memória" técnica do projeto, consolidando as regras arquiteturais, padrões de código e decisões de design tomadas para garantir assertividade em futuras manutenções e evoluções.

## 🏗️ Arquitetura e Organização (Clean Architecture)

O projeto segue os princípios da Clean Architecture, dividindo as responsabilidades em camadas concêntricas onde a dependência aponta sempre para dentro (em direção ao domínio).

### Camadas do Projeto (`src/`)
-   **`domain/`**: Coração da aplicação. Contém as entidades de negócio (Pydantic Models) e as interfaces (Contratos). **Regra**: Não pode importar nada de outras camadas.
    -   `models/`: Modelos de dados (ex: `client.py`, `transaction.py`).
    -   `interfaces/`: Contratos definitivos (`repositories/`, `providers/`).
-   **`application/`**: Casos de uso e orquestração.
    -   `usecases/`: Lógica que coordena o fluxo entre domínio e infraestrutura (ex: `webhook_processor.py`).
-   **`infra/`**: Detalhes de implementação e ferramentas externas.
    -   `core/`: Configurações globais, Logger e Dependências (DI).
    -   `data/`: Persistência de dados, Repositórios concretos, Migrations.
    -   `providers/`: Integrações com APIs externas (ex: MercadoPago, Santander).
-   **`presentation/`**: Interface com o mundo externo (FastAPI Routes, ViewModels).

---

## 📏 Padrões de Código e Convenções

### interface Naming
-   Todas as interfaces (classes abstratas) **devem** ser prefixadas com a letra `I`.
    -   ✅ Correto: `IClientRepository`, `IWebhookProvider`.
    -   ❌ Incorreto: `ClientRepositoryInterface`.
-   Os arquivos de interface também seguem o prefixo `i` minúsculo.
    -   Ex: `iclient_repository.py`.

### Folder Naming (Anti-Redundância)
-   Evite nomes redundantes como `infra/infra.core`. Utilize nomes diretos e semânticos.
    -   ✅ Correto: `infra/core`, `infra/data`, `infra/providers`.

### Model Splitting
-   **Nunca** use um arquivo `models.py` único e monolítico.
-   Divida os modelos por domínio de negócio dentro de `domain/models/`.
-   Use `__init__.py` para exportar os modelos e facilitar as importações externas.

---

## 🛠️ Gerenciamento de Banco de Dados

### Migrations (Alembic)
-   Localização: `src/infra/data/migrations/`.
-   As migrations devem usar o driver `asyncpg` (configurado no `env.py`).
-   A configuração do Alembic (`alembic.ini`) deve ser mantida simplificada, apontando para o caminho interno na `src`.


### CLI Unificada
Para evitar confusão entre ferramentas, use o script `cli.py` centralizado:
```bash
# Setup completo (Migration + Seed)
python3 -m src.infra.data.cli setup

# Apenas Migrations
python3 -m src.infra.data.cli migrate

# Reverter alteração
python3 -m src.infra.data.cli rollback
```

---

## 🧩 Padrões de Design Implementados

### Strategy Pattern (Webhooks)
-   Utilizado para suportar múltiplos provedores de pagamento.
-   Cada provedor implementa `IWebhookProvider`.
-   O `WebhookProcessor` recebe uma instância concreta do provedor via Injeção de Dependência no momento da rota.

### Repository Pattern
-   Desacopla a lógica de acesso a dados da lógica de negócio.
-   O código de aplicação depende de `ITransactionRepository` (interface), não da implementação `TransactionRepository` (concreta).

---

## 🚀 Próximos Passos e Guardrails
1.  **Sempre** verifique se a nova funcionalidade requer uma interface no `domain/interfaces/`.
2.  **Sempre** atualize o `cli.py` se for necessário um novo tipo de automação de banco.
3.  **Sempre** mantenha o Logger padronizado em `src/infra/core/logger.py`.
