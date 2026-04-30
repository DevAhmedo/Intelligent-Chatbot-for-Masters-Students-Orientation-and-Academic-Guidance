# Mosaed — Intelligent Chatbot for Master's Students

Mosaed is an AI chatbot built for master's students at the University of Sharjah. It answers questions about academic regulations, thesis procedures, registration deadlines, program requirements, and more using RAG (Retrieved Augmented Generation). All responses are grounded in official UOS documents.

## What it does

- Answers student questions using Retrieval-Augmented Generation (RAG) over official UOS PDFs
- Maintains conversation history for context-aware follow-up questions
- Rewrites follow-up questions into standalone queries before searching
- Refuses out-of-scope questions (e.g. general knowledge, unrelated topics)
- Supports Arabic and English questions
- Organizes chats into sessions and folders
- Provides a landing page, login/signup, and authenticated chat experience

## Tech Stack

### Language & Runtime
- **Python 3.11** — backend and RAG pipeline
- **Node.js 18+** — frontend build tooling

### Frontend
- **React 18** + **Vite** — UI framework and build tool
- **CSS Modules** — component-scoped styling
- **React Router** — client-side navigation between pages

### Backend
- **FastAPI** — async REST API
- **PostgreSQL** — stores users, sessions, messages, folders, and feedback
- **SQLAlchemy (async)** — ORM for database access
- **JWT (python-jose)** + **bcrypt** — authentication and password hashing

### RAG Pipeline
- **ChromaDB** — vector database for storing and searching document embeddings
- **Ollama (nomic-embed-text)** — local embedding model
- **Groq API (Llama 4 scout)** — cloud LLM for generating answers and rewriting queries
- **LangChain + Docling** — PDF loading, Markdown conversion, and chunking

### Documents (data sources)
- Master's Executive Regulations
- Roadmap for Master's Students (Arabic + English)
- Student Handbook
- Academic Calendar 2026–2027
- Master's Seminar materials

## Project Structure

```
├── RAG/                    # RAG pipeline (embeddings, querying, DB population)
├── backend/                # FastAPI app (routes, services, database models)
├── frontend/               # React + Vite app
├── services/               # Groq LLM client
├── data/                   # Source PDF documents
└── chroma_db/              # Vector database (local only, not in repo)
```
