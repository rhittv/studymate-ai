# StudyMate AI 📚

An AI study assistant that lets users upload PDF notes and ask questions grounded in the document text.

## Features

- Upload and process multiple text-based PDFs
- Extract text with `pypdf`
- Split documents into overlapping chunks
- Retrieve relevant passages with a simple keyword baseline
- Generate context-grounded answers with the OpenAI API
- Inspect retrieved source passages in the interface
- Keep a short conversation history for follow-up questions

## Tech stack

- Python
- Streamlit
- OpenAI API
- pypdf
- python-dotenv

## Run locally

### 1. Requirements

Install Python 3.10 or newer and Git.

### 2. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/studymate-ai.git
cd studymate-ai
```

### 3. Create and activate a virtual environment

**macOS / Linux**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure your API key

Copy `.env.example` to `.env`, then replace the placeholder with your own OpenAI API key.

Never commit `.env` or share your API key publicly.

### 6. Start the app

```bash
streamlit run app.py
```

Your browser should open the local app, usually at `http://localhost:8501`.

## How it works

1. PDF text is extracted.
2. Text is split into overlapping chunks.
3. A basic keyword retrieval function selects passages related to the question.
4. The selected passages are sent to the LLM as context.
5. The model answers and can refer to retrieved chunk IDs.
6. The user can inspect the retrieved passages in the interface.

## Current limitations

This is an intentionally small first version, not a production-grade RAG system.

- Keyword retrieval is a baseline; it is not semantic search.
- Scanned/image-only PDFs need OCR.
- Citations refer to text chunks, not yet precise PDF page links.
- Conversation and uploaded documents live in the current Streamlit session.
- No authentication or persistent database is included.
- LLM answers can still be incorrect; verify important information against the source documents.

## Roadmap

- [ ] Improve PDF parsing and preserve page-level citations
- [ ] Add semantic embeddings and vector search
- [ ] Add a document library and session persistence
- [ ] Add tests for chunking, retrieval, and API error handling
- [ ] Add answer-quality evaluation
- [ ] Deploy a public demo
- [ ] Add screenshots and a short demo video

## Portfolio note

This project demonstrates a first end-to-end LLM application: interface, file processing, retrieval, API integration, and basic source inspection. The roadmap documents the next engineering improvements.
