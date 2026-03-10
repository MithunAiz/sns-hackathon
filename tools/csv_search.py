"""
tools/csv_search.py
-------------------
Tool for searching the guest list CSV file (data/guests.csv).
Used by the AI agent to look up attendees by name, role, organization,
RSVP status, or dietary preference.
"""

import os
from typing import List, Dict, Any

import pandas as pd


# Path to the guests CSV file (relative to project root)
CSV_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "guests.csv")


def _load_csv() -> pd.DataFrame:
    """
    Load the guests CSV file into a pandas DataFrame.

    Returns:
        pd.DataFrame: The guest list with all columns loaded as strings
        to ensure consistent searching across all fields.

    Raises:
        FileNotFoundError: If guests.csv does not exist at the expected path.
    """
    # Load all columns as string type for uniform text searching
    return pd.read_csv(CSV_FILE, dtype=str).fillna("")


def search_csv(query: str) -> List[Dict[str, Any]]:
    """
    Search the guest list CSV for rows matching the given query string.

    Performs a case-insensitive search across ALL columns of the CSV.
    A row is included in the results if any of its field values contains
    the query string.

    Args:
        query (str): The search term or phrase to look for in the guest list.

    Returns:
        List[Dict[str, Any]]: A list of matching guest records as dictionaries.
        Each dict contains keys: Name, Role, Organization, Email,
        RSVP_Status, Dietary_Preference.
        Returns an empty list if no rows match.

    Example:
        >>> results = search_csv("Speaker")
        >>> for r in results:
        ...     print(r["Name"], "-", r["Role"])
        'Dr. Ananya Krishnan - Keynote Speaker'
        'James Rutherford - Panelist'
    """
    df = _load_csv()
    query_lower = query.lower().strip()

    # Build a boolean mask: True if ANY column in the row contains the query
    mask = df.apply(
        lambda row: row.str.lower().str.contains(query_lower, na=False).any(),
        axis=1
    )

    matched_df = df[mask]

    # Return results as a list of plain dictionaries
    return matched_df.to_dict(orient="records")