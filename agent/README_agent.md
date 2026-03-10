# Agent Layer — README

## Purpose
The agent layer is the brain of the project. It uses **Anthropic Claude**
with function calling to intelligently decide which tool(s) to search
based on the user's natural language query.

## Files
| File | Purpose |
|------|---------|
| `agent.py` | Core agentic loop — calls tools, synthesizes answers |
| `tool_registry.py` | Tool definitions in Anthropic function-calling format |
| `__init__.py` | Exports `run_agent` for backend use |

## How It Works
1. User sends a query like *"What did we decide about catering?"*
2. Claude reads the tool descriptions and decides to call `search_notes` + `search_email`
3. Results are returned to Claude
4. Claude synthesizes a final answer citing the sources

## Usage
```python
from agent import run_agent

result = run_agent("Who is the keynote speaker?")
print(result["answer"])
print(result["sources"])  # ['search_email', 'search_pdf']
```