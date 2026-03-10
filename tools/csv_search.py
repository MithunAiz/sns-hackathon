# DEVELOPER 4: Data Tools & Resources
# Tool to search and filter CSV structures.

import os

_DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "guests.csv")


def search_csv(query: str) -> str:
    """
    Loads guests.csv with pandas and returns rows where any cell value
    contains a keyword from the query (case-insensitive).

    Returns a formatted table of matching rows, or lists all rows when no
    keyword matches (so a generic 'guest list' question still returns data).
    """
    try:
        import pandas as pd
    except ImportError:
        return "[csv_search] pandas is not installed. Run: pip install pandas"

    try:
        df = pd.read_csv(_DATA_FILE)
    except FileNotFoundError:
        return f"[csv_search] CSV file not found at: {_DATA_FILE}"
    except Exception as exc:
        return f"[csv_search] Could not read CSV: {exc}"

    keywords = [w.lower() for w in query.split() if len(w) > 2]

    # Search across all string columns.
    mask = df.apply(
        lambda col: col.astype(str).str.lower().str.contains(
            "|".join(keywords), regex=True
        ) if keywords else col.notna()
    ).any(axis=1)

    result_df = df[mask] if mask.any() else df  # Fall back to full list.

    if result_df.empty:
        return "No matching guests found."

    return result_df.to_string(index=False)
