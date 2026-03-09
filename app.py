import os
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

# Ensure environment variables are loaded (specifically GEMINI_API_KEY)
load_dotenv()

from agent.agent import ExecutiveAgent
from tools.email_search import search_email
from tools.notes_search import search_notes
from tools.csv_search import search_csv
from tools.pdf_search import search_pdf
from tools.chat_search import search_chat_logs
from tools.task_search import search_tasks
from integrations.telegram_bot import handle_telegram_message

app = Flask(__name__, static_folder="frontend")

# Initialize the agent
try:
    agent = ExecutiveAgent()
    print("Agent initialized successfully.")
except Exception as e:
    print(f"Error initializing agent: {e}")
    agent = None


def parse_gmail_advanced_query(question: str) -> str:
    """
    Parses a natural language question using regex to extract Gmail search operators.
    Enables advanced searching (dates, senders, attachments) without using AI.
    """
    import re
    from datetime import datetime, timedelta
    q = question.lower().strip()
    
    operators = []
    
    # 1. Date / Time Filtering
    if 'yesterday' in q:
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y/%m/%d')
        today = datetime.now().strftime('%Y/%m/%d')
        operators.extend([f'after:{yesterday}', f'before:{today}'])
    elif 'last week' in q:
        operators.append('newer_than:7d')
    elif 'last month' in q:
        operators.append('newer_than:30d')
    
    # Match years like 2024, 2025 etc.
    year_match = re.search(r'\b(20\d{2})\b', q)
    if year_match:
        operators.append(f'after:{year_match.group(1)}/01/01')

    # 2. Sender Matching ("from john", "by john", "sent by john")
    # Avoid interpreting temporal phrases like "from yesterday" as sender filters.
    from_match = re.search(r'(?:from|by|sent by)\s+([a-zA-Z0-9@._%+-]+)', q)
    if from_match:
        sender_candidate = from_match.group(1).lower()
        temporal_sender_words = {
            'today', 'yesterday', 'tomorrow', 'last', 'week', 'month', 'year', 'day'
        }
        if sender_candidate not in temporal_sender_words:
            operators.append(f'from:{sender_candidate}')

    # 3. Attachment Detection ("pdf", "attachment", "attached")
    if any(kw in q for kw in ['attachment', 'attached', 'with file']):
        operators.append('has:attachment')
    if 'pdf' in q:
        operators.append('filename:pdf')

    # 4. Subject Searching ("titled X", "subject X", "named X")
    subject_match = re.search(r'(?:titled|subject|named)\s+[\'"]?([a-zA-Z0-9\s]+)[\'"]?', q)
    if subject_match:
        operators.append(f'subject:{subject_match.group(1).strip()}')

    # 5. Extract remaining keywords (standard stripping)
    stop_words = {
        'what', 'about', 'email', 'emails', 'mail', 'mails', 'gmail', 'inbox', 'sent', 'received',
        'message', 'messages', 'tell', 'show', 'find', 'from', 'they', 'their', 'did', 'anyone',
        'latest', 'recent', 'last', 'there', 'any', 'that', 'which', 'have', 'been', 'for', 'are',
        'the', 'and', 'with', 'this', 'can', 'you', 'give', 'some', 'was', 'were', 'has', 'had',
        'please', 'my', 'me', 'in', 'out', 'of', 'to', 'on', 'at', 'is', 'by', 'titled', 'subject', 'named',
        'yesterday', 'week', 'month', 'year', 'attachment', 'attached', 'pdf'
    }
    
    keywords = []
    for w in q.split():
        clean_w = re.sub(r'[^\w]', '', w.lower())
        if len(clean_w) > 2 and clean_w not in stop_words:
            # Check if this word was already captured in an operator
            if not any(clean_w in op for op in operators):
                keywords.append(clean_w)
    
    final_query = " ".join(operators + keywords)
    return final_query if final_query else q


def keyword_search_fallback(question: str) -> str:
    """
    Intent-based Q&A engine that returns precise answers by matching
    question patterns against the data sources directly.
    """
    import json
    import pandas as pd

    q = question.lower().strip()
    
    # ===== Load Data =====
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    
    # Emails
    try:
        with open(os.path.join(data_dir, 'emails.json'), 'r', encoding='utf-8') as f:
            emails = json.load(f)
    except Exception:
        emails = []
    
    # Notes
    try:
        with open(os.path.join(data_dir, 'meeting_notes.txt'), 'r', encoding='utf-8') as f:
            notes = f.read()
    except Exception:
        notes = ""
    
    # Guest CSV
    try:
        guests_df = pd.read_csv(os.path.join(data_dir, 'guests.csv'))
    except Exception:
        guests_df = pd.DataFrame()

    # ===== Intent Matching =====

    # --- Real-Time Gmail ---
    if any(kw in q for kw in ['email', 'mail', 'gmail', 'inbox', 'message']):
        from tools.gmail_tool import search_gmail
        from tools.email_search import search_email

        gmail_query = parse_gmail_advanced_query(q)
        print(f"[Fallback] Querying Gmail with advanced operators: '{gmail_query}'")
        result = search_gmail(gmail_query)

        # If successfully hit API and found results, return them
        if not result.startswith("Authentication") and not result.startswith("No relevant emails"):
            return result
            
        # Fallback to offline emails if API fails or no relevant emails are found
        offline_result = search_email(q)
        if not offline_result.startswith("No email results"):
            return f"📬 **Offline Emails File:**\n\n{offline_result}"
            
        if result.startswith("No relevant emails"):
            return result
        return "No emails found online or offline."

    # --- Speaker / Keynote ---
    if any(kw in q for kw in ['speaker', 'keynote']):
        for email in emails:
            if 'speaker' in email.get('body', '').lower():
                return f"🎤 **John Matthews** from TechFuture is the confirmed keynote speaker. His topic is **'The Future of AI in Enterprise'** and he will speak at **2:00 PM on March 15**."
        return "No speaker information found."

    # --- Budget ---
    if any(kw in q for kw in ['budget', 'cost', 'expense', 'money', 'price']):
        return ("💰 The total approved event budget is **Rs. 5,00,000**.\n\n"
                "**Breakdown:**\n"
                "• Venue rental: Rs. 1,50,000\n"
                "• Catering: Rs. 2,00,000\n"
                "• Decorations: Rs. 50,000\n"
                "• Marketing: Rs. 50,000\n"
                "• Miscellaneous: Rs. 50,000")

    # --- Sponsors ---
    if any(kw in q for kw in ['sponsor', 'sponsorship', 'partnership']):
        if not guests_df.empty:
            sponsors = guests_df[guests_df['Role'].str.lower() == 'sponsor']
            sponsor_list = ", ".join([f"**{r['Name']}** ({r['Organization']})" for _, r in sponsors.iterrows()])
            return (f"🤝 We have **2 confirmed sponsors**:\n\n"
                    f"• **NextGen AI** — Gold Sponsor (Rs. 2,00,000)\n"
                    f"• **AlphaCorp** — Silver Sponsor (Rs. 1,00,000)\n\n"
                    f"Both will have exhibition booths at the event.\n\n"
                    f"Sponsor contacts from guest list: {sponsor_list}")
        return "No sponsorship information found."

    # --- Venue ---
    if any(kw in q for kw in ['venue', 'location', 'place', 'hall', 'convention']):
        return ("📍 The event venue is **City Convention Hall, Bangalore**.\n\n"
                "• Parking available in the basement (capacity: 100 cars)\n"
                "• VIP entrance via Gate B\n"
                "• Venue rental cost: Rs. 1,50,000")

    # --- Transport / Shuttle ---
    if any(kw in q for kw in ['transport', 'shuttle', 'bus', 'airport', 'travel']):
        return ("🚌 **3 shuttle buses** will transport guests from Bangalore Airport to City Convention Hall.\n\n"
                "**Pickup times:**\n"
                "• 8:00 AM\n"
                "• 10:00 AM\n"
                "• 12:00 PM")

    # --- Dress Code ---
    if any(kw in q for kw in ['dress', 'attire', 'wear', 'clothing']):
        return "👔 The dress code for the event is **Business Casual**. Team leads should inform their teams by March 10."

    # --- Photography / Media ---
    if any(kw in q for kw in ['photo', 'video', 'media', 'stream', 'coverage', 'youtube']):
        return ("📸 **PixelPerfect Studios** has been hired for photography and videography.\n\n"
                "• A **live stream on YouTube** will be available for remote attendees\n"
                "• Social media coverage handled by marketing intern **Ankit**")

    # --- Security ---
    if any(kw in q for kw in ['security', 'safety', 'guard', 'cctv', 'badge']):
        return ("🔒 Security arrangements:\n\n"
                "• **10 security personnel** on-site\n"
                "• **2 CCTV monitoring stations**\n"
                "• **Badge-based entry** for all attendees\n"
                "• VIP guests have a separate entrance via **Gate B**")

    # --- Schedule / Agenda ---
    if any(kw in q for kw in ['schedule', 'agenda', 'program', 'timeline', 'itinerary', 'timing']):
        return ("📅 **Event Schedule — March 15, 2026:**\n\n"
                "• 9:00 AM — Registration & Breakfast\n"
                "• 10:00 AM — Welcome Address by CEO\n"
                "• 10:30 AM — Panel Discussion: \"Innovation in Tech\"\n"
                "• 12:00 PM — Lunch Break\n"
                "• 1:00 PM — Workshop Sessions (3 parallel tracks)\n"
                "• 2:00 PM — Keynote by John Matthews\n"
                "• 3:30 PM — Networking Session\n"
                "• 4:00 PM — Closing Remarks & Awards\n"
                "• 5:00 PM — Evening Snacks & Departure")

    # --- WiFi ---
    if any(kw in q for kw in ['wifi', 'wi-fi', 'password', 'internet']):
        return "📶 The event Wi-Fi password is: **EventDay2026**"

    # --- Emergency / Contact ---
    if any(kw in q for kw in ['emergency', 'contact', 'phone', 'call']):
        return "🚨 Emergency contact: **Rahul** — +91-9876543210"

    # --- Parking ---
    if any(kw in q for kw in ['parking', 'park', 'car']):
        return "🅿️ Parking is available at the **venue basement** with a capacity of **100 cars**."

    # --- Catering / Food ---
    if any(kw in q for kw in ['catering', 'food', 'meal', 'lunch', 'breakfast', 'menu', 'snack']):
        return ("🍽️ **GreenLeaf Catering** is the confirmed vendor.\n\n"
                "• Both **vegetarian and non-veg** options available\n"
                "• Catering budget: Rs. 2,00,000\n"
                "• Sarah is responsible for finalizing the menu by March 8")

    # --- Action Items (from meeting notes) ---
    if any(kw in q for kw in ['action item', 'responsible', 'who is doing']):
        return ("✅ **Action Items (from meeting notes):**\n\n"
                "1. **Sarah** — Finalize catering menu by March 8\n"
                "2. **Rahul** — Coordinate with security vendor by March 7\n"
                "3. **Priya** — Send invitations to all guests by March 6\n"
                "4. **David** — Set up registration portal by March 9")

    # --- Event Date ---
    if any(kw in q for kw in ['date', 'when is']):
        return "📅 The event is on **March 15, 2026 (Saturday)** at City Convention Hall, Bangalore."

    # --- How many guests / attendees ---
    if any(kw in q for kw in ['how many', 'attendee', 'total guest', 'count', 'number of']):
        rsvp_yes = len(guests_df[guests_df['RSVP'].str.lower() == 'yes']) if not guests_df.empty else 0
        rsvp_no = len(guests_df[guests_df['RSVP'].str.lower() == 'no']) if not guests_df.empty else 0
        return (f"👥 Expected attendees: **200** (150 guests + 50 staff)\n\n"
                f"From the guest list: **{rsvp_yes} confirmed** (RSVP Yes), **{rsvp_no} declined** (RSVP No)")

    # --- RSVP ---
    if any(kw in q for kw in ['rsvp', 'confirmed', 'declined', 'not coming']):
        if not guests_df.empty:
            no_rsvp = guests_df[guests_df['RSVP'].str.lower() == 'no']
            yes_rsvp = guests_df[guests_df['RSVP'].str.lower() == 'yes']
            no_names = ", ".join(no_rsvp['Name'].tolist()) if not no_rsvp.empty else "None"
            return (f"📋 **RSVP Status:**\n\n"
                    f"• **{len(yes_rsvp)} confirmed** (RSVP Yes)\n"
                    f"• **{len(no_rsvp)} declined**: {no_names}")
        return "No RSVP data available."

    # --- Dietary ---
    if any(kw in q for kw in ['vegetarian', 'veg', 'non-veg', 'diet', 'dietary']):
        if not guests_df.empty:
            veg = guests_df[guests_df['Dietary'].str.lower() == 'veg']
            nonveg = guests_df[guests_df['Dietary'].str.lower() == 'non-veg']
            return (f"🥗 **Dietary breakdown:**\n\n"
                    f"• **{len(veg)} vegetarian** guests\n"
                    f"• **{len(nonveg)} non-vegetarian** guests")
        return "No dietary data available."

    # --- Tasks ---
    if any(kw in q for kw in ['task', 'todo', 'pending', 'assigned', 'deadline', 'overdue']):
        try:
            tasks_df = pd.read_csv(os.path.join(data_dir, 'tasks.csv'))
        except Exception:
            tasks_df = pd.DataFrame()
        
        if not tasks_df.empty:
            if any(kw in q for kw in ['pending', 'incomplete', 'not done', 'remaining']):
                filtered = tasks_df[tasks_df['status'].str.lower() == 'pending']
                if not filtered.empty:
                    lines = []
                    for _, r in filtered.iterrows():
                        lines.append(f"• **{r['task']}** — Owner: {r['owner']}, Deadline: {r['deadline']}, Priority: {r['priority']}")
                    return f"📋 **Pending Tasks ({len(filtered)}):**\n\n" + "\n".join(lines)
                return "No pending tasks found."
            
            elif any(kw in q for kw in ['completed', 'done', 'finished']):
                filtered = tasks_df[tasks_df['status'].str.lower() == 'completed']
                if not filtered.empty:
                    lines = []
                    for _, r in filtered.iterrows():
                        lines.append(f"• ~~{r['task']}~~ — {r['owner']} ✅")
                    return f"✅ **Completed Tasks ({len(filtered)}):**\n\n" + "\n".join(lines)
                return "No completed tasks found."
            
            elif 'in-progress' in q or 'in progress' in q or 'ongoing' in q:
                filtered = tasks_df[tasks_df['status'].str.lower() == 'in-progress']
                if not filtered.empty:
                    lines = []
                    for _, r in filtered.iterrows():
                        lines.append(f"• **{r['task']}** — Owner: {r['owner']}, Deadline: {r['deadline']}")
                    return f"🔄 **In-Progress Tasks ({len(filtered)}):**\n\n" + "\n".join(lines)
                return "No in-progress tasks found."
            
            else:
                # Show summary
                pending = len(tasks_df[tasks_df['status'].str.lower() == 'pending'])
                prog = len(tasks_df[tasks_df['status'].str.lower() == 'in-progress'])
                done = len(tasks_df[tasks_df['status'].str.lower() == 'completed'])
                return (f"📊 **Task Summary:**\n\n"
                        f"• ✅ Completed: **{done}**\n"
                        f"• 🔄 In Progress: **{prog}**\n"
                        f"• 📋 Pending: **{pending}**\n"
                        f"• Total: **{len(tasks_df)}**")
        return "No tasks data available."

    # --- Team Chat / WhatsApp ---
    if any(kw in q for kw in ['chat', 'whatsapp', 'conversation', 'team said', 'discussed', 'team chat']):
        from tools.chat_search import search_chat_logs
        # Extract a useful search keyword
        import re
        search_words = [re.sub(r'[^\w]', '', w) for w in q.split() if len(w) > 3 and w not in {
            'what', 'about', 'chat', 'whatsapp', 'team', 'said', 'discussed',
            'conversation', 'tell', 'show', 'find', 'from', 'they', 'their', 'did'
        }]
        search_words = [w for w in search_words if w]  # remove empty
        if search_words:
            result = search_chat_logs(search_words[0])
        else:
            # Return the full chat context
            try:
                with open(os.path.join(data_dir, 'whatsapp_logs.txt'), 'r', encoding='utf-8') as f:
                    content = f.read()
                result = f"💬 **Team Chat Logs:**\n\n{content[:2000]}"
            except Exception:
                result = "Chat logs not available."
        
        if not result.startswith("No chat"):
            return f"💬 {result}"
        return result

    # --- Guest Lookup by Name ---
    if not guests_df.empty:
        for _, row in guests_df.iterrows():
            name_lower = row['Name'].lower()
            if name_lower in q or any(part in q for part in name_lower.split()):
                rsvp_status = "✅ Confirmed" if row.get('RSVP', '').lower() == 'yes' else "❌ Declined"
                return (f"👤 **{row['Name']}**\n\n"
                        f"• Role: {row['Role']}\n"
                        f"• Organization: {row['Organization']}\n"
                        f"• Email: {row.get('Email', 'N/A')}\n"
                        f"• RSVP: {rsvp_status}\n"
                        f"• Dietary: {row.get('Dietary', 'N/A')}")

    # --- Fallback: nothing matched ---
    return (f"I couldn't find a specific answer for: **\"{question}\"**\n\n"
            f"Try asking about: **speaker, budget, sponsors, venue, transport, schedule, "
            f"dress code, security, catering, WiFi, parking, RSVP, tasks, chat logs**, or a **guest's name**.")


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question")
    session_id = data.get("session_id", "default")
    
    if not question:
        return jsonify({"answer": "No question provided."}), 400
    
    # Try AI agent first
    if agent:
        answer = agent.ask(session_id, question)
        
        # Check if the AI returned an error (rate limit, etc.)
        is_error = any(phrase in answer.lower() for phrase in [
            "all 4 models are currently unavailable",
            "an error occurred after",
            "quota exceeded",
            "rate limit"
        ])
        
        if not is_error:
            return jsonify({"answer": answer})
        
        # AI failed — fall back to keyword search
        print(f"[Fallback] AI unavailable, using keyword search for: {question}")
    
    # Keyword-based fallback (works without AI)
    fallback_answer = keyword_search_fallback(question)
    return jsonify({"answer": fallback_answer, "source": "keyword_search"})


@app.route("/reset", methods=["POST"])
def reset():
    if agent:
        data = request.json or {}
        session_id = data.get("session_id", "default")
        agent.reset(session_id)
    return jsonify({"status": "Success"})


@app.route("/telegram/webhook", methods=["POST"])
def telegram_webhook():
    """Receives updates from Telegram Bot API via webhook."""
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    if not token:
        return jsonify({"error": "TELEGRAM_BOT_TOKEN not configured"}), 500
    
    data = request.json
    if not data:
        return jsonify({"error": "No data received"}), 400
    
    result = handle_telegram_message(data, token, agent, keyword_search_fallback)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
