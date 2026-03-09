document.addEventListener('DOMContentLoaded', () => {
    // ===== DOM References =====
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const chatScroll = document.getElementById('chat-scroll');
    const sendBtn = document.getElementById('send-btn');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebar-overlay');
    const toggleSidebarBtn = document.getElementById('toggle-sidebar');
    const newChatBtn = document.getElementById('new-chat-btn');
    const resetBtn = document.getElementById('reset-btn');
    const historyList = document.getElementById('history-list');

    // ===== State =====
    let currentSessionId = null;
    let chats = JSON.parse(localStorage.getItem('chats')) || {};

    // ===== SVG Icons =====
    const aiAvatarSVG = `<svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>`;
    const userAvatarSVG = `<svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`;
    const chatIconSVG = `<svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>`;

    // ===== Utility =====
    function generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substring(2, 7);
    }

    function formatText(text) {
        let f = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        f = f.replace(/\*(.*?)\*/g, '<em>$1</em>');
        f = f.replace(/`([^`]+)`/g, '<code class="bg-black/30 px-1.5 py-0.5 rounded text-xs font-mono">$1</code>');
        f = f.replace(/\n/g, '<br>');
        return f;
    }

    function scrollToBottom() {
        requestAnimationFrame(() => {
            chatScroll.scrollTop = chatScroll.scrollHeight;
        });
    }

    // ===== Mobile Sidebar Toggle =====
    if (toggleSidebarBtn) {
        toggleSidebarBtn.addEventListener('click', () => {
            sidebar.classList.toggle('open');
            sidebarOverlay.classList.toggle('hidden');
        });
    }

    // ===== Render Messages =====
    function createAIMessage(text) {
        const wrapper = document.createElement('div');
        wrapper.className = 'flex items-start gap-3 msg-animate';
        wrapper.innerHTML = `
            <div class="w-8 h-8 rounded-full bg-accent-light flex items-center justify-center flex-shrink-0 mt-1 shadow-md">
                ${aiAvatarSVG}
            </div>
            <div class="bg-[#2f2f2f] text-gray-200 rounded-2xl rounded-tl-md px-4 py-3 max-w-[75%] text-sm leading-relaxed shadow-sm">
                ${formatText(text)}
            </div>
        `;
        chatBox.appendChild(wrapper);
        scrollToBottom();
    }

    function createUserMessage(text) {
        const wrapper = document.createElement('div');
        wrapper.className = 'flex justify-end msg-animate';
        wrapper.innerHTML = `
            <div class="bg-accent text-white rounded-2xl rounded-tr-md px-4 py-3 max-w-[75%] text-sm leading-relaxed shadow-sm">
                ${formatText(text)}
            </div>
        `;
        chatBox.appendChild(wrapper);
        scrollToBottom();
    }

    function showTypingIndicator() {
        const wrapper = document.createElement('div');
        wrapper.id = 'typing-indicator';
        wrapper.className = 'flex items-start gap-3 msg-animate';
        wrapper.innerHTML = `
            <div class="w-8 h-8 rounded-full bg-accent-light flex items-center justify-center flex-shrink-0 mt-1 shadow-md">
                ${aiAvatarSVG}
            </div>
            <div class="bg-[#2f2f2f] rounded-2xl rounded-tl-md px-5 py-4 shadow-sm flex items-center gap-1.5">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
        `;
        chatBox.appendChild(wrapper);
        scrollToBottom();
        userInput.disabled = true;
        sendBtn.disabled = true;
    }

    function removeTypingIndicator() {
        const el = document.getElementById('typing-indicator');
        if (el) el.remove();
        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.focus();
    }

    // ===== Sidebar / History =====
    function updateSidebar() {
        historyList.innerHTML = '';
        const sorted = Object.values(chats).sort((a, b) => b.updatedAt - a.updatedAt);
        sorted.forEach(chat => {
            const item = document.createElement('button');
            item.className = `w-full flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-left truncate transition-colors duration-150 ${chat.id === currentSessionId ? 'bg-sidebar-hover text-white' : 'text-gray-400 hover:bg-sidebar-hover hover:text-gray-200'}`;
            item.innerHTML = `${chatIconSVG}<span class="truncate">${chat.title}</span>`;
            item.addEventListener('click', () => {
                loadSession(chat.id);
                if (window.innerWidth < 768) {
                    sidebar.classList.remove('open');
                    sidebarOverlay.classList.add('hidden');
                }
            });
            historyList.appendChild(item);
        });
    }

    // ===== Session Management =====
    function createNewSession() {
        currentSessionId = generateId();
        chats[currentSessionId] = {
            id: currentSessionId,
            title: 'New Chat',
            messages: [],
            updatedAt: Date.now()
        };
        saveChats();
        chatBox.innerHTML = '';
        createAIMessage("Hello! I'm your Executive Assistant. I can search through your emails, notes, guest lists, and event plans. Ask me anything!");
        updateSidebar();

        fetch('/reset', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: currentSessionId })
        }).catch(console.error);
    }

    function loadSession(id) {
        if (!chats[id]) return;
        currentSessionId = id;
        chatBox.innerHTML = '';
        createAIMessage("Hello! I'm your Executive Assistant. I can search through your emails, notes, guest lists, and event plans. Ask me anything!");
        chats[id].messages.forEach(msg => {
            if (msg.sender === 'user') createUserMessage(msg.text);
            else createAIMessage(msg.text);
        });
        updateSidebar();
    }

    function saveChats() {
        localStorage.setItem('chats', JSON.stringify(chats));
    }

    function addMessageToSession(text, sender) {
        if (!currentSessionId || !chats[currentSessionId]) return;
        const chat = chats[currentSessionId];
        chat.messages.push({ text, sender });
        chat.updatedAt = Date.now();
        if (chat.messages.length === 1 && sender === 'user') {
            chat.title = text.length > 28 ? text.substring(0, 28) + '…' : text;
            updateSidebar();
        }
        saveChats();
    }

    // ===== Initialize =====
    if (Object.keys(chats).length === 0) {
        createNewSession();
    } else {
        const recent = Object.values(chats).sort((a, b) => b.updatedAt - a.updatedAt)[0];
        loadSession(recent.id);
    }
    updateSidebar();

    // ===== Event Listeners =====
    newChatBtn.addEventListener('click', createNewSession);

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = userInput.value.trim();
        if (!question) return;
        if (!currentSessionId) createNewSession();

        createUserMessage(question);
        addMessageToSession(question, 'user');
        userInput.value = '';
        showTypingIndicator();

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question, session_id: currentSessionId })
            });
            const data = await response.json();
            removeTypingIndicator();
            if (response.ok) {
                createAIMessage(data.answer);
                addMessageToSession(data.answer, 'bot');
            } else {
                createAIMessage(`⚠️ Error: ${data.answer}`);
            }
        } catch (error) {
            removeTypingIndicator();
            createAIMessage("⚠️ Could not connect to the server. Please make sure the backend is running.");
            console.error(error);
        }
    });

    resetBtn.addEventListener('click', () => {
        if (confirm('Delete all chat history? This cannot be undone.')) {
            localStorage.removeItem('chats');
            chats = {};
            currentSessionId = null;
            createNewSession();
        }
    });
});
