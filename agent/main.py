"""
Ask My Notes — Agent
Checks local notes first, then falls back to web search.
Uses Groq API for fast reasoning.
"""

import argparse
import json
import sys
from pathlib import Path

# Runtime imports with graceful degradation
GROQ_AVAILABLE = False
DDGS_AVAILABLE = False
Groq = None  # type: ignore
DDGS = None  # type: ignore

try:
    from groq import Groq  # type: ignore
    GROQ_AVAILABLE = True
except ImportError:
    pass

# Import local search function
try:
    from search_docs import search_docs
except ImportError as e:
    print(f"Error: Cannot import search_docs: {e}")
    sys.exit(1)

# Try optional web search
try:
    from duckduckgo_search import DDGS  # type: ignore
    DDGS_AVAILABLE = True
except ImportError:
    pass

# =============================================================================
# CONFIGURATION
# =============================================================================

MODEL_ID = "llama-3.3-70b-versatile"
MODEL_API_KEY = "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"

# Initialize client only if Groq is available
client = None
if GROQ_AVAILABLE:
    client = Groq(api_key=MODEL_API_KEY)
else:
    print("Warning: groq package not installed. Install with: pip install groq")

# =============================================================================
# TOOLS
# =============================================================================

def search_local_notes(query: str) -> str:
    """Search local notes folder for relevant content."""
    print(f"\n[Tool] Searching local notes for: {query}")
    result = search_docs(query)
    print(f"[Tool] Result: {result[:120]}")
    return result


def search_web(query: str) -> str:
    """Search the web using DuckDuckGo."""
    if not DDGS_AVAILABLE:
        return "Web search not available (duckduckgo_search not installed)."
    
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


# Tool schemas for Groq
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_local_notes",
            "description": "Search local notes folder for relevant content related to the query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query to find relevant notes"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

if DDGS_AVAILABLE:
    TOOLS.append({
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for current information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Web search query"
                    }
                },
                "required": ["query"]
            }
        }
    })

# Mapping of tool names to functions
TOOL_FUNCTIONS = {
    "search_local_notes": search_local_notes,
    "search_web": search_web,
}


# =============================================================================
# AGENT
# =============================================================================

def run_agent(query: str) -> None:
    """Run the agent with tool use."""
    if not client:
        print("Error: groq client not initialized. Install groq with: pip install groq")
        return
    
    print(f"\nQuery: {query}")
    print("=" * 60)
    
    messages = [
        {
            "role": "user",
            "content": query
        }
    ]
    
    # Agentic loop
    max_iterations = 5
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        print(f"\n[Iteration {iteration}]")
        
        # Call Groq with tool use
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=messages,
            tools=TOOLS if TOOLS else None,
            tool_choice="auto" if TOOLS else None,
            temperature=0.7,
            max_tokens=1024,
        )
        
        # Check stop reason
        choice = response.choices[0]
        
        if choice.finish_reason == "tool_calls":
            # Model wants to use a tool
            assistant_message = {
                "role": "assistant",
                "content": choice.message.content or "",
                "tool_calls": choice.message.tool_calls
            }
            messages.append(assistant_message)
            
            # Process each tool call
            tool_results = []
            for tool_call in choice.message.tool_calls:
                tool_name = tool_call.function.name
                tool_input = json.loads(tool_call.function.arguments)
                
                print(f"\n  Calling: {tool_name}({tool_input})")
                
                # Execute tool
                if tool_name in TOOL_FUNCTIONS:
                    result = TOOL_FUNCTIONS[tool_name](**tool_input)
                else:
                    result = f"Unknown tool: {tool_name}"
                
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_call.id,
                    "content": result,
                })
            
            # Add tool results to messages
            messages.append({
                "role": "user",
                "content": tool_results
            })
            
        else:
            # Model has finished (no more tool calls)
            print("\n[Agent Response]")
            print("=" * 60)
            print(choice.message.content)
            break
    
    if iteration >= max_iterations:
        print(f"\nReached max iterations ({max_iterations})")


def main():
    parser = argparse.ArgumentParser(
        description="Ask My Notes — Agent that searches local notes and the web"
    )
    parser.add_argument(
        "query",
        nargs="?",
        default="What is in my notes?",
        help="Question to ask the agent",
    )
    args = parser.parse_args()
    
    run_agent(args.query)


if __name__ == "__main__":
    main()