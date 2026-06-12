"""
Ask My Notes — Agent
Checks local notes first, then falls back to web search.
"""

import argparse
import json
from duckduckgo_search import DDGS
from search_docs import search_docs

try:
    from groq import Groq
except ImportError as exc:
    raise ImportError("Run: pip install groq") from exc

# =============================================================================
# CONFIGURATION
# =============================================================================

MODEL_ID = "llama-3.3-70b-versatile"
MODEL_API_KEY = "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"

client = Groq(api_key=MODEL_API_KEY)

# =============================================================================
# TOOLS
# =============================================================================

def search_local_notes(query: str) -> str:
    print(f"\n[Tool] Searching local notes for: {query}")
    result = search_docs(query)
    print(f"[Tool] Result: {result[:120]}")
    return result

def search_web(query: str) -> str:
    print(f"\n[Tool] Searching web for: {query}")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        if not results:
            return "No web results found."
        output = []
        for r in results:
            output.append(f"Title: {r['title']}\nSnippet: {r['body']}\nURL: {r['href']}")
        return "\n\n".join(output)
    except Exception as e:
        return f"Web search failed: {e}"

# Tool schemas Groq understands
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_local_notes",
            "des