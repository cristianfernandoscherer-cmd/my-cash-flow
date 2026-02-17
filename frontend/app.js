// Configuration
const API_BASE_URL = 'http://localhost:8080'; // Support service URL
const HEALTH_CHECK_INTERVAL = 30000; // 30 seconds

// Session Management
class SessionManager {
    constructor() {
        this.sessionId = this.getOrCreateSessionId();
        this.clientId = this.getOrCreateClientId();
    }

    getOrCreateSessionId() {
        let sessionId = localStorage.getItem('chat_session_id');
        if (!sessionId) {
            sessionId = this.generateId();
            localStorage.setItem('chat_session_id', sessionId);
        }
        return sessionId;
    }

    getOrCreateClientId() {
        let clientId = localStorage.getItem('chat_client_id');
        if (!clientId) {
            clientId = this.generateId();
            localStorage.setItem('chat_client_id', clientId);
        }
        return clientId;
    }

    generateId() {
        return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }

    resetSession() {
        this.sessionId = this.generateId();
        localStorage.setItem('chat_session_id', this.sessionId);
    }
}

// Chat Application
class ChatApp {
    constructor() {
        this.sessionManager = new SessionManager();
        this.messageContainer = document.getElementById('chat-messages');
        this.messageInput = document.getElementById('message-input');
        this.chatForm = document.getElementById('chat-form');
        this.sendButton = document.getElementById('send-button');
        this.connectionStatus = document.getElementById('connection-status');
        this.sessionDisplay = document.getElementById('session-display');

        this.isConnected = false;
        this.isSending = false;

        this.init();
    }

    init() {
        // Display session ID
        this.sessionDisplay.textContent = this.sessionManager.sessionId.substr(0, 12) + '...';

        // Event listeners
        this.chatForm.addEventListener('submit', (e) => this.handleSubmit(e));

        // Check connection
        this.checkHealth();
        setInterval(() => this.checkHealth(), HEALTH_CHECK_INTERVAL);
    }

    async checkHealth() {
        try {
            const response = await fetch(`${API_BASE_URL}/health`);
            const data = await response.json();

            if (data.status === 'alive') {
                this.setConnectionStatus(true);
            } else {
                this.setConnectionStatus(false);
            }
        } catch (error) {
            console.error('Health check failed:', error);
            this.setConnectionStatus(false);
        }
    }

    setConnectionStatus(connected) {
        this.isConnected = connected;
        this.connectionStatus.textContent = connected ? 'Online' : 'Offline';
        this.connectionStatus.style.color = connected ? '#4ade80' : '#f87171';
    }

    async handleSubmit(e) {
        e.preventDefault();

        const message = this.messageInput.value.trim();
        if (!message || this.isSending) return;

        // Add user message to UI
        this.addMessage(message, 'user');
        this.messageInput.value = '';

        // Show loading indicator
        const loadingId = this.showLoading();

        try {
            this.isSending = true;
            this.sendButton.disabled = true;

            const response = await fetch(`${API_BASE_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionManager.sessionId,
                    client_id: this.sessionManager.clientId
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Remove loading indicator
            this.removeLoading(loadingId);

            // Add bot response
            this.addMessage(data.resposta || 'Desculpe, não consegui processar sua mensagem.', 'bot');

        } catch (error) {
            console.error('Error sending message:', error);
            this.removeLoading(loadingId);
            this.addMessage('Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente.', 'bot', true);
        } finally {
            this.isSending = false;
            this.sendButton.disabled = false;
            this.messageInput.focus();
        }
    }

    addMessage(text, sender, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';

        if (sender === 'bot') {
            const img = document.createElement('img');
            img.src = 'chris-avatar.png';
            img.alt = 'Bot Avatar';
            avatar.appendChild(img);
        } else {
            const img = document.createElement('img');
            img.src = 'user-avatar.png';
            img.alt = 'User Avatar';
            avatar.appendChild(img);
        }

        const contentWrapper = document.createElement('div');

        const content = document.createElement('div');
        content.className = 'message-content';

        if (sender === 'bot') {
            // For bot messages, we allow HTML (for <br>) and convert newlines
            let formattedText = text.replace(/\n/g, '<br>');
            // Handle markdown bold (**text** -> <b>text</b>)
            formattedText = formattedText.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
            content.innerHTML = formattedText;
        } else {
            // For user messages, keep as text for safety
            content.textContent = text;
        }

        if (isError) {
            content.style.background = 'linear-gradient(135deg, #f87171 0%, #ef4444 100%)';
        }

        const time = document.createElement('div');
        time.className = 'message-time';
        time.textContent = new Date().toLocaleTimeString('pt-BR', {
            hour: '2-digit',
            minute: '2-digit'
        });

        contentWrapper.appendChild(content);
        contentWrapper.appendChild(time);

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(contentWrapper);

        this.messageContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    showLoading() {
        const loadingId = `loading-${Date.now()}`;
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'loading-message message bot';
        loadingDiv.id = loadingId;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        const img = document.createElement('img');
        img.src = 'chris-avatar.png';
        img.alt = 'Bot Avatar';
        avatar.appendChild(img);

        const dots = document.createElement('div');
        dots.className = 'loading-dots';
        dots.innerHTML = '<span></span><span></span><span></span>';

        loadingDiv.appendChild(avatar);
        loadingDiv.appendChild(dots);

        this.messageContainer.appendChild(loadingDiv);
        this.scrollToBottom();

        return loadingId;
    }

    removeLoading(loadingId) {
        const loadingElement = document.getElementById(loadingId);
        if (loadingElement) {
            loadingElement.remove();
        }
    }

    scrollToBottom() {
        this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
});
