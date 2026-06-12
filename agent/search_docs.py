"""
search_docs.py — Local file indexer for Ask My Notes
Reads .txt files from the notes/ folder and searches them for relevant content.
"""

import os

NOTES_FOLDER = os.path.join(os.path.dirname(__file__), "notes")


def search_docs(query: str) -> str:
    """
    Search local notes folder for content relevant to the query.
    Returns matching text snippets, or a message if nothing found.
    """
    if not os.path.exists(NOTES_FOLDER):
        return "No notes folder found."

    query_words = query.lower().split()
    results = []

    for filename in os.listdir(NOTES_FOLDER):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(NOTES_FOLDER, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(word in line_lower for word in query_words):
                # Grab a small chunk around the matching line
                start = max(0, i - 1)
                end = min(len(lines), i + 3)
                chunk = "".join(lines[start:end]).strip()
                results.append(f"[From {filename}]:\n{chunk}")

    if not results:
        return "No relevant content found in local notes."

    return "\n\n---\n\n".join(results[:5])  # Return top 5 matches