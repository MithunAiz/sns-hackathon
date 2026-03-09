import os


def search_chat_logs(query: str) -> str:
    """
    Search whatsapp_logs.txt for relevant chat messages based on the query.
    Returns matching lines with surrounding context.
    """
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'whatsapp_logs.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return "Error: whatsapp_logs.txt not found."

    results = []
    query_lower = query.lower()

    for i, line in enumerate(lines):
        if query_lower in line.lower():
            # Include one line of context before and after the match
            start = max(0, i - 1)
            end = min(len(lines), i + 2)
            context = "".join(lines[start:end]).strip()
            results.append(context)

    if not results:
        return f"No chat messages found matching query: '{query}'"

    # Deduplicate overlapping contexts
    unique = list(dict.fromkeys(results))
    return "Found in team chat logs:\n\n" + "\n\n---\n\n".join(unique)
