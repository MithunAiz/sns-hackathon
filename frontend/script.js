const API_URL = "http://localhost:5000";
let sessionId = "session_" + Date.now();

const SOURCE_MAP = {
  search_email: "src-email",
  search_notes: "src-notes",
  search_csv:   "src-csv",
  search_pdf:   "src-pdf"
};

const SOURCE_LABELS = {
  search_email: "📧 Emails",
  search_notes: "📝 Meeting Notes",
  search_csv:   "📊 Guest List",
  search_pdf:   "📄 Event PDF"
};

function fillQuery(text) {
  document.getElementById("queryInput").value = text;
  document.getElementById("queryInput").focus();
}

function addMessage(role, text, sources = []) {
  const messages = document.getElementById("messages");

  const msg = document.createElement("div");
  msg.className = `message ${role === "user" ? "user-message" : "agent-message"}`;

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = role === "user" ? "🧑" : "🤖";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerHTML = text.replace(/\n/g, "<br>");

  if (sources.length > 0) {
    const tagsDiv = document.createElement("div");
    tagsDiv.className = "sources-tag";
    sources.forEach(s => {
      const tag = document.createElement("span");
      tag.className = "source-tag";
      tag.textContent = SOURCE_LABELS[s] || s;
      tagsDiv.appendChild(tag);
    });
    bubble.appendChild(tagsDiv);
  }

  msg.appendChild(avatar);
  msg.appendChild(bubble);
  messages.appendChild(msg);
  messages.scrollTop = messages.scrollHeight;
}

function addTyping() {
  const messages = document.getElementById("messages");
  const msg = document.createElement("div");
  msg.className = "message agent-message";
  msg.id = "typing-indicator";

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = "🤖";

  const bubble = document.createElement("div");
  bubble.className = "bubble typing";
  bubble.innerHTML = "<span></span><span></span><span></span>";

  msg.appendChild(avatar);
  msg.appendChild(bubble);
  messages.appendChild(msg);
  messages.scrollTop = messages.scrollHeight;
}

function removeTyping() {
  const el = document.getElementById("typing-indicator");
  if (el) el.remove();
}

function highlightSources(sources) {
  // Reset all
  document.querySelectorAll(".source-item").forEach(el => {
    el.classList.remove("active");
  });
  // Highlight used ones
  sources.forEach(s => {
    const id = SOURCE_MAP[s];
    if (id) document.getElementById(id)?.classList.add("active");
  });
}

async function sendQuery() {
  const input = document.getElementById("queryInput");
  const btn = document.getElementById("sendBtn");
  const query = input.value.trim();
  if (!query) return;

  addMessage("user", query);
  input.value = "";
  btn.disabled = true;
  addTyping();

  try {
    const response = await fetch(`${API_URL}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, session_id: sessionId })
    });

    const data = await response.json();
    removeTyping();

    if (data.error) {
      addMessage("agent", "Sorry, I encountered an error: " + data.error);
    } else {
      addMessage("agent", data.answer, data.sources || []);
      highlightSources(data.sources || []);
    }

  } catch (err) {
    removeTyping();
    addMessage("agent", "Could not connect to the agent server. Make sure the backend is running on port 5000.");
  }

  btn.disabled = false;
  input.focus();
}

async function resetChat() {
  await fetch(`${API_URL}/reset`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId })
  });

  sessionId = "session_" + Date.now();
  document.querySelectorAll(".source-item").forEach(el => el.classList.remove("active"));

  const messages = document.getElementById("messages");
  messages.innerHTML = `
    <div class="message agent-message">
      <div class="avatar">🤖</div>
      <div class="bubble">
        Hello! I'm your Personal Executive Agent. I can search across your
        <strong>emails, meeting notes, guest list, and event documents</strong>
        to find any information instantly. What would you like to know?
      </div>
    </div>`;
}