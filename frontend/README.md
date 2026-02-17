# My Cash Flow - Frontend Chat

Uma aplicação frontend moderna e elegante para interagir com o serviço de suporte do My Cash Flow.

## 🎨 Features

- ✨ Interface moderna com tema dark mode
- 💬 Chat em tempo real com o serviço de suporte
- 🔄 Gerenciamento automático de sessão
- 📱 Design responsivo (mobile-friendly)
- 🎭 Animações suaves e efeitos glassmorphism
- 🔌 Verificação automática de conexão
- ⚡ Indicador de carregamento durante processamento

## 🚀 Como Usar

### Pré-requisitos

- Serviço `support` rodando em `http://localhost:8001`
- Navegador web moderno (Chrome, Firefox, Safari, Edge)

### Executando a Aplicação

**Opção 1: Docker (Recomendado)**
```bash
# Na raiz do projeto
docker-compose up frontend

# Acesse http://localhost:3000 no navegador
```

**Opção 2: Abrir diretamente no navegador**
   ```bash
   # Navegue até o diretório frontend
   cd frontend
   
   # Abra o index.html no seu navegador
   open index.html  # macOS
   xdg-open index.html  # Linux
   start index.html  # Windows
   ```

**Opção 3: Usar um servidor HTTP simples**
   ```bash
   # Com Python 3
   cd frontend
   python3 -m http.server 8080
   
   # Acesse http://localhost:8080 no navegador
   ```

   ```bash
   # Com Node.js (npx http-server)
   cd frontend
   npx http-server -p 8080
   
   # Acesse http://localhost:8080 no navegador
   ```

### Configuração

Se o serviço `support` estiver rodando em uma URL diferente, edite o arquivo `app.js`:

```javascript
const API_BASE_URL = 'http://localhost:8001'; // Altere para sua URL
```

## 📁 Estrutura do Projeto

```
frontend/
├── index.html      # Estrutura HTML da aplicação
├── styles.css      # Estilos CSS com tema dark mode
├── app.js          # Lógica JavaScript e integração com API
└── README.md       # Este arquivo
```

## 🎯 Funcionalidades Técnicas

### Session Management
- Gera automaticamente `session_id` e `client_id` únicos
- Persiste sessão no `localStorage` do navegador
- Mantém histórico de conversas durante a sessão

### API Integration
- Endpoint: `POST /chat`
- Payload:
  ```json
  {
    "message": "sua mensagem",
    "session_id": "id-da-sessao",
    "client_id": "id-do-cliente"
  }
  ```
- Health check automático a cada 30 segundos

### Error Handling
- Tratamento de erros de rede
- Mensagens de erro amigáveis ao usuário
- Indicador visual de status de conexão

## 🎨 Design

- **Tema**: Dark mode com gradientes vibrantes
- **Cores primárias**: Roxo (#667eea) e Rosa (#764ba2)
- **Tipografia**: Inter (Google Fonts)
- **Efeitos**: Glassmorphism, sombras suaves, animações CSS

## 🔧 Troubleshooting

### Chat não conecta
- Verifique se o serviço `support` está rodando
- Confirme a URL no `app.js`
- Verifique o console do navegador para erros

### CORS Error
- O serviço `support` precisa ter CORS habilitado
- Adicione no `app.py` do support:
  ```python
  from fastapi.middleware.cors import CORSMiddleware
  
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```

## 📝 Licença

Este projeto faz parte do My Cash Flow.
