# My Cash Flow 💰

Sistema inteligente de controle financeiro pessoal composto por microsserviços, utilizando LLMs para classificação automática de gastos e assistente financeiro via chat.

## 🚀 Visão Geral dos Serviços

O projeto é dividido em dois microsserviços principais:

### 1. Balance (Transações & Ingestão) 💸
Responsável por registrar e categorizar todo o fluxo financeiro.
- **Funcionalidade**: Recebe mensagens de um grupo no **Telegram** sobre gastos ou entradas.
- **Fluxo**: Telegram Webhook → API Balance → **LLM (Classificação)** → Banco de Dados.
- **Objetivo**: Automatizar a inserção de dados financeiros a partir de linguagem natural.

### 2. Support (Assistente Financeiro) 🤖
Atua como um consultor financeiro inteligente.
- **Funcionalidade**: Chat interativo onde o usuário pode tirar dúvidas sobre suas finanças.
- **Tecnologia**: Utiliza **LangGraph** para orquestrar agentes autônomos.
- **Fluxo**: Usuário → Support API → Agentes LangGraph → Consulta API Balance (quando necessário) → Resposta.

## 🏗️ Arquitetura e Tecnologias

O sistema é orquestrado via **Docker Compose** e utiliza as seguintes tecnologias:

- **Linguagem**: Python 3.12+
- **Framework Web**: FastAPI
- **Banco de Dados**: PostgreSQL (Drivers: `asyncpg`)
- **Cache/Mensageria**: Redis
- **IA/LLM**: OpenAI (GPT-4o), LangChain, LangGraph
- **Infraestrutura**: Docker, Docker Compose

### Estrutura do Projeto
```text
my-cash-flow/
├── balance/           # Serviço de Ingestão e Transações
├── support/           # Serviço de Assistente (LangGraph)
├── docker-compose.yml # Orquestração dos contêineres
├── Makefile           # Atalhos para comandos comuns
```

## 🚀 Como Executar

A maneira recomendada de rodar o projeto é utilizando Docker Compose.

### Pré-requisitos
- Docker e Docker Compose
- Chave da OpenAI configurada no `.env`

### Passos
1. Clone o repositório.
2. Configure as variáveis de ambiente:
   ```bash
   cp .env.example .env
   # Edite o .env com suas credenciais (OPENAI_API_KEY, DB config, etc)
   ```
3. Inicie os serviços:
   ```bash
   docker-compose up --build
   ```

> [!IMPORTANT]
> O serviço **Balance** roda na porta `8081` e o **Support** na porta `8082` (ou `8080` via docker internamente, verifique o `docker-compose.yml`).

## 🧪 Testes e Qualidade

O projeto mantém um alto padrão de qualidade com testes automatizados e verificação de cobertura.

### Comandos do Makefile

| Comando | Descrição |
| :--- | :--- |
| `make install` | Instala dependências de ambos os serviços. |
| `make test` | Executa todos os testes unitários. |
| `make test-balance` | Testes do serviço Balance. |
| `make test-support` | Testes do serviço Support. |
| `make coverage` | Relatório de cobertura de código. |

### Cobertura e Pre-commit
Mantemos uma cobertura mínima de **90%** para ambos os serviços. Um *pre-commit hook* garante que nenhum código com cobertura insuficiente seja commitado.

**Instalar o hook de verificação:**
```bash
cp scripts/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## 📚 Documentação Técnica
- **Balance**: Segue Clean Architecture (Domain, Application, Infra, Presentation).
- **Support**: Baseado em grafos de agentes com LangGraph.

Consulte a pasta `docs/` em cada serviço para mais detalhes específicos.
