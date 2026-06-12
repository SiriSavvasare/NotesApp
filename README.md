# 📝 Ask My Notes

> **Local-first intelligence that searches your private documents before touching the internet.**

Built for the **Mozilla.ai Hackathon** — using `tinyagent`, `Groq (llama-3.3-70b)`, and `DuckDuckGo` as a web fallback.

![Local First](https://img.shields.io/badge/Local--First-Privacy%20Focused-7c6af7?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.12-3ecf8e?style=flat-square&logo=python)
![Groq](https://img.shields.io/badge/LLM-Groq%20llama--3.3--70b-f59e0b?style=flat-square)
![Mozilla.ai](https://img.shields.io/badge/Track-Mozilla.ai-ff6611?style=flat-square)

---

## 🧠 What is Ask My Notes?

Stop searching through disorganized folders. **Ask My Notes** lets you talk directly to your college notes, research documents, and meeting logs through an intelligent agent.

Your data **never leaves your machine**. The web is only used when your notes don't have the answer.

```
You ask a question
        ↓
  Search local notes first
        ↓
  Found? ──→ Answer from your notes 📝
        ↓
  Not found? ──→ Web search fallback 🌐
```

---

## ✨ Key Features

- 🔒 **Local-First** — Your files stay on your device. Zero cloud dependency, zero data leakage
- 🔁 **Hybrid Intelligence** — Seamlessly falls back to the web only when local notes can't answer
- 🧭 **Transparent Sourcing** — Always tells you whether the answer came from your notes or the web
- ♿ **Accessible AI** — Built with neurodiversity in mind; upcoming features for visual learning and adaptive pacing
- ⚡ **Fast** — Groq's inference runs at 1000+ tokens/sec on the same llama model as llamafile

---

## 🏗️ Technical Architecture

| Component | Role | Our Implementation |
|---|---|---|
| **encoderfile** | Embeds local docs into vector spaces | `search_docs.py` keyword search |
| **llamafile** | Local LLM inference | Groq API (`llama-3.3-70b-versatile`) |
| **mcpd / MCP** | Bridge to open web tools | `duckduckgo-search` via tool calling |
| **any-agent / tinyagent** | Orchestrator brain | `tinyagent` + Groq tool calling |

> **Note on our pivot:** The original spec uses `llamafile` for fully local inference. Our hardware couldn't run the model locally, so we substituted Groq's cloud API which runs the **identical `llama-3.3-70b` model**. The architecture and privacy philosophy remain the same.

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/SiriSavvasare/NotesApp
cd NotesApp
```

### 2. Set up Python environment

```bash
python -m venv venv312
# Windows
venv312\Scripts\activate
# Mac/Linux
source venv312/bin/activate
```

### 3. Install dependencies

```bash
pip install groq duckduckgo-search mozilla-ai-tinyagent
```

### 4. Add your notes

Drop your `.txt` files into the `notes/` folder:

```
NotesApp/
├── agent/
│   ├── main.py
│   ├── search_docs.py
│   └── ask_my_notes_ui.html
└── notes/
    ├── your_notes.txt
    ├── lecture_notes.txt
    └── any_text_file.txt
```

### 5. Set your Groq API key

Get a free key at [console.groq.com](https://console.groq.com), then open `agent/main.py` and set:

```python
MODEL_API_KEY = "your_groq_api_key_here"
```

### 6. Run the agent

```bash
python agent/main.py "What is supervised learning?"
```

---

## 💬 Example Queries

```bash
# Answers from your local notes
python agent/main.py "What did I write about neural networks?"
python agent/main.py "What are my project ideas for the hackathon?"
python agent/main.py "How do I use list comprehensions in Python?"

# Falls back to web search
python agent/main.py "What is the current Groq rate limit?"
python agent/main.py "Who won the 2024 Nobel Prize in Physics?"
```

---

## 🖥️ UI

Open `agent/ask_my_notes_ui.html` in your browser for a full chat interface:

- Browse your notes in the sidebar
- See real-time tool traces (which tool was called)
- Green tag = answered from local notes
- Yellow tag = answered from web

---

## 📁 Project Structure

```
NotesApp/
├── agent/
│   ├── main.py              # Main agent with Groq + tool calling
│   ├── search_docs.py       # Local notes keyword search
│   └── ask_my_notes_ui.html # Browser UI
├── notes/                   # Drop your .txt files here
│   ├── ml_notes.txt
│   ├── python_cheatsheet.txt
│   ├── project_ideas.txt
│   ├── mozilla_ai_track.txt
│   └── groq_setup.txt
├── .gitignore
└── README.md
```

---

## 🛠️ Built With

- [Mozilla.ai tinyagent](https://github.com/mozilla-ai/any-agent) — Agent orchestration
- [Groq](https://groq.com) — Fast LLM inference (llama-3.3-70b-versatile)
- [DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/) — Privacy-respecting web fallback
- Python 3.12

---

## 🌱 Roadmap

- [ ] PDF support via PyMuPDF
- [ ] Semantic search using vector embeddings
- [ ] Full local mode when llamafile hardware support improves
- [ ] Voice input via whisper.cpp
- [ ] Visual learning aids for neurodiverse users

---

## 👩‍💻 Built by

**Siri Savvasare** — built with passion for accessible, sovereign, and intelligent education.

*Mozilla.ai Hackathon 2025*
