# DEVELOPER 3: AI Agent Logic
# Responsibilities:
# - interpret user queries
# - select appropriate tool
# - call tool functions
# - generate final answer using LLM

from agent.tool_registry import select_tool, call_tool

def process_question(question: str) -> str:
    """
    Main entry point for evaluating a user question.
    Expected workflow:
    1. Understand query
    2. Select Tool
    3. Query Data Source
    4. Compile Final Answer
    """
    
    # STUB IMPLEMENTATION
    tool_name = select_tool(question)
    tool_result = call_tool(tool_name, question)
    
    # TODO: Pass the result to an LLM to generate natural language answer
    final_answer = f"[Agent processed via {tool_name}] Found data: {tool_result}"
    return final_answer
