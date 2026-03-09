import pandas as pd
import os

def search_csv(query: str) -> str:
    """
    Search guests.csv using pandas for any rows that match the query.
    Returns the matching rows as a string.
    """
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'guests.csv')
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        return "Error: guests.csv not found."
    
    query_lower = query.lower()
    
    # Filter rows: check if any cell in the row contains the query as substring
    mask = df.astype(str).apply(lambda col: col.str.contains(query_lower, case=False, na=False))
    matched_df = df[mask.any(axis=1)]
    
    if matched_df.empty:
        return f"No guests found matching query: '{query}'"
    
    return f"Found details in guest list:\n{matched_df.to_string(index=False)}"
