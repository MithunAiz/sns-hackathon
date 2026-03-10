# ── agent.py ──────────────────────────────────────────────────────────────────
# DEVELOPER 3: AI Agent Logic
# Responsibilities:
# - interpret user queries
# - select the appropriate data tool
# - call the tool to retrieve relevant context
# - pass context + question to an LLM and return a natural-language answer
#
# LLM priority:
#   1. Google Gemini  (set GEMINI_API_KEY in .env)
#   2. OpenAI GPT     (set OPENAI_API_KEY in .env)
#   3. Fallback       (returns raw tool data when no API key is available)
# ──────────────────────────────────────────────────────────────────────────────

import os
import logging

from dotenv import load_dotenv
from agent.tool_registry import select_tool, call_tool

# Load .env so API keys are available whether the agent is called via Flask
# (server_config also calls this) or directly in tests/scripts.
load_dotenv()

logger = logging.getLogger(__name__)

# ── Prompt template ────────────────────────────────────────────────────────────
# Instructs the LLM to answer using only the retrieved context.
_PROMPT_TEMPLATE = """You are a helpful executive assistant.
Use ONLY the information provided in the context below to answer the question.
If the context does not contain enough information, say so clearly.

Context:
{context}

Question: {question}

Answer:"""


# ── LLM helpers ───────────────────────────────────────────────────────────────

def _call_gemini(prompt: str) -> str | None:
    """Call Google Gemini. Returns None if the package/key is unavailable or quota exceeded."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash-lite")
        response = model.generate_content(prompt)
        return response.text.strip()
    except ImportError:
        logger.warning("google-generativeai package not installed. Run: pip install google-generativeai")
        return None
    except Exception as exc:
        err_str = str(exc)
        if "429" in err_str or "quota" in err_str.lower():
            logger.warning("Gemini quota exceeded — falling back to next LLM. Reset your quota or enable billing at console.cloud.google.com")
        else:
            logger.error("Gemini API error: %s", exc)
        return None


def _call_openai(prompt: str) -> str | None:
    """Call OpenAI ChatCompletion. Returns None if the package/key is unavailable."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()
    except ImportError:
        logger.warning("openai package not installed. Run: pip install openai")
        return None
    except Exception as exc:
        logger.error("OpenAI API error: %s", exc)
        return None


def _generate_answer(question: str, context: str) -> str:
    """
    Try Gemini → OpenAI → fallback (raw context).
    Returns the first successful LLM response.
    """
    prompt = _PROMPT_TEMPLATE.format(context=context, question=question)

    answer = _call_gemini(prompt)
    if answer:
        logger.info("Answer generated via Gemini")
        return answer

    answer = _call_openai(prompt)
    if answer:
        logger.info("Answer generated via OpenAI")
        return answer

    # No LLM available — return the raw tool data with a clear label.
    logger.warning("No LLM API key configured. Returning raw tool context.")
    return f"[Raw data — configure GEMINI_API_KEY or OPENAI_API_KEY for natural language answers]\n\n{context}"


# ── Main entry point ───────────────────────────────────────────────────────────

def process_question(question: str) -> str:
    """
    Full pipeline:
      1. Select the best tool for the question
      2. Retrieve relevant context from that data source
      3. Ask the LLM to produce a natural-language answer
      4. Return the answer string
    """
    logger.info("process_question called: %s", question)

    # Step 1 – Tool selection
    tool_name = select_tool(question)
    logger.info("Tool selected: %s", tool_name)

    # Step 2 – Data retrieval
    context = call_tool(tool_name, question)
    logger.info("Tool returned %d chars of context", len(context))

    # Step 3 & 4 – LLM synthesis
    answer = _generate_answer(question, context)
    return answer
