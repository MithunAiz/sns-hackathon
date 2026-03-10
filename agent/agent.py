"""
agent/agent.py
Context-Aware Personal Executive Agent
Works without API credits using direct tool search.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools import search_email, search_notes, search_csv, search_pdf


def run_agent(user_query: str, conversation_history: list = []) -> dict:
    """Smart agent that searches correct data source based on query."""
    query_lower = user_query.lower()
    sources_used = []
    results = []

    if any(w in query_lower for w in ["catering", "food", "menu", "vendor", "greenleaf"]):
        sources_used += ["search_notes", "search_email"]
        notes = search_notes("catering")
        emails = search_email("catering")
        results.append("📝 From Meeting Notes:\n" + "\n".join(notes[:3]))
        if emails:
            results.append("📧 From Emails:\n" + emails[0]["subject"] + "\n" + emails[0]["body"][:300])

    elif any(w in query_lower for w in ["speaker", "keynote", "ananya", "presentation"]):
        sources_used += ["search_email", "search_pdf"]
        emails = search_email("keynote speaker")
        pdf = search_pdf("keynote")
        if emails:
            results.append("📧 From Emails:\n" + emails[0]["subject"] + "\n" + emails[0]["body"][:300])
        if pdf:
            results.append("📄 From Event PDF:\n" + "\n".join(pdf[:2]))

    elif any(w in query_lower for w in ["guest", "attendee", "rsvp", "confirmed", "count", "how many"]):
        sources_used.append("search_csv")
        confirmed = search_csv("Confirmed")
        all_guests = search_csv("")
        results.append(f"📊 From Guest List:\nTotal confirmed guests: {len(confirmed)}")
        for g in confirmed[:5]:
            results.append(f"  • {g['Name']} | {g['Role']} | {g['Organization']}")

    elif any(w in query_lower for w in ["transport", "shuttle", "parking", "bus", "valet"]):
        sources_used += ["search_email", "search_notes"]
        emails = search_email("transport")
        notes = search_notes("transport")
        if emails:
            results.append("📧 From Emails:\n" + emails[0]["body"][:400])
        if notes:
            results.append("📝 From Meeting Notes:\n" + "\n".join(notes[:3]))

    elif any(w in query_lower for w in ["budget", "cost", "money", "finance", "total"]):
        sources_used.append("search_notes")
        notes = search_notes("budget")
        results.append("📝 From Meeting Notes:\n" + "\n".join(notes[:5]))

    elif any(w in query_lower for w in ["venue", "location", "hall", "city convention"]):
        sources_used += ["search_notes", "search_pdf"]
        notes = search_notes("venue")
        pdf = search_pdf("venue")
        results.append("📝 From Meeting Notes:\n" + "\n".join(notes[:3]))
        if pdf:
            results.append("📄 From Event PDF:\n" + "\n".join(pdf[:2]))

    elif any(w in query_lower for w in ["schedule", "timing", "time", "agenda"]):
        sources_used.append("search_pdf")
        pdf = search_pdf("schedule")
        results.append("📄 From Event PDF:\n" + "\n".join(pdf[:4]))

    elif any(w in query_lower for w in ["sponsor", "techcorp", "ai ventures"]):
        sources_used += ["search_notes", "search_pdf"]
        notes = search_notes("sponsor")
        results.append("📝 From Meeting Notes:\n" + "\n".join(notes[:3]))

    else:
        sources_used += ["search_email", "search_notes"]
        emails = search_email(user_query)
        notes = search_notes(user_query)
        if emails:
            results.append("📧 From Emails:\n" + emails[0]["subject"] + "\n" + emails[0]["body"][:200])
        if notes:
            results.append("📝 From Meeting Notes:\n" + "\n".join(notes[:3]))

    answer = "\n\n".join(results) if results else "No relevant information found. Try asking about catering, speakers, guests, transport, budget, or venue."

    return {
        "answer": answer,
        "sources": list(set(sources_used)),
        "history": conversation_history
    }