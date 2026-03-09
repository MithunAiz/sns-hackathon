import os
import time
from datetime import datetime
import google.generativeai as genai
from agent.tool_registry import get_tools

# Fallback chain of models â€” each has its own separate quota
FALLBACK_MODELS = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
]

SYSTEM_INSTRUCTION = (
    "You are a Context-Aware Personal Executive Agent. "
    f"Today's date is {datetime.now().strftime('%Y-%m-%d')}. "
    "You have access to several tools that search your real-time Gmail inbox, old offline emails, meeting notes, "
    "a guest CSV, a PDF event plan, WhatsApp team chat logs, and a task tracker. "
    "When the user asks a question, determine which tool(s) to use, call them to get the text context, "
    "and then answer the user's question clearly and concisely based on the retrieved information. "
    "If the tools do not provide the answer, say you could not find the information in the provided documents. "
    "When quoting emails, summarize the relevant points."
)

class ExecutiveAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
            
        genai.configure(api_key=api_key)
        
        # Pre-initialize a GenerativeModel for each fallback model
        self.tools = get_tools()
        self.models = {}
        for model_name in FALLBACK_MODELS:
            self.models[model_name] = genai.GenerativeModel(
                model_name=model_name,
                tools=self.tools,
                system_instruction=SYSTEM_INSTRUCTION
            )
        
        # Sessions store: { session_id: { model_name: chat_instance } }
        self.sessions = {}
        
    def _get_chat(self, session_id: str, model_name: str):
        """Gets or creates a chat instance for a specific session and model."""
        if session_id not in self.sessions:
            self.sessions[session_id] = {}
        
        if model_name not in self.sessions[session_id]:
            model = self.models[model_name]
            self.sessions[session_id][model_name] = model.start_chat(
                enable_automatic_function_calling=True
            )
        
        return self.sessions[session_id][model_name]

    def ask(self, session_id: str, query: str) -> str:
        """
        Send a query to the agent, falling back through different models
        if one hits its rate limit or fails.
        """
        errors = []
        
        for model_name in FALLBACK_MODELS:
            try:
                chat = self._get_chat(session_id, model_name)
                print(f"[Agent] Trying model: {model_name}")
                response = chat.send_message(query)
                print(f"[Agent] Success with model: {model_name}")
                return response.text
            except Exception as e:
                error_msg = str(e)
                errors.append(f"{model_name}: {error_msg}")
                print(f"[Agent] Model {model_name} failed: {error_msg}")
                
                # Small delay before trying next model
                time.sleep(1)
                continue
        
        # All models failed
        summary = "\n".join(errors)
        return (
            f"All {len(FALLBACK_MODELS)} models are currently unavailable. "
            f"This is likely due to API rate limits. Please wait a minute and try again.\n\n"
            f"Details:\n{summary}"
        )

    def reset(self, session_id: str):
        """Resets the chat history for a specific session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
