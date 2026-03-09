import pandas as pd
import os


def search_tasks(query: str) -> str:
    """
    Search tasks.csv for tasks matching the query.
    Returns the matching task rows as a formatted string.
    """
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tasks.csv')
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        return "Error: tasks.csv not found."

    query_lower = query.lower()

    # Filter rows: check if any cell in the row contains the query as substring
    mask = df.astype(str).apply(lambda col: col.str.contains(query_lower, case=False, na=False))
    matched_df = df[mask.any(axis=1)]

    if matched_df.empty:
        return f"No tasks found matching query: '{query}'"

    return f"Found in task tracker:\n{matched_df.to_string(index=False)}"
