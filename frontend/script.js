// DEVELOPER 1: Frontend Logic
// Responsibilities:
// - send user messages to backend
// - display assistant responses
// - maintain chat history

async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    if (!message) return;

    // Display user message in chat history
    appendMessage('You', message, 'user-msg');
    userInput.value = '';

    // Placeholder POST request to /ask
    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: message })
        });
        const data = await response.json();
        
        // Display AI response
        appendMessage('Agent', data.answer, 'agent-msg');
    } catch (error) {
        console.error('Error fetching response:', error);
        appendMessage('System', 'Error communicating with server.', 'agent-msg');
    }
}

function appendMessage(sender, text, className) {
    const chatHistory = document.getElementById('chat-history');
    const msgElement = document.createElement('div');
    msgElement.className = `msg ${className}`;
    msgElement.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatHistory.appendChild(msgElement);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}
