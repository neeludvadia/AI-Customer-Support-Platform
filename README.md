# AI Customer Support Platform 🤖💼

Welcome to the **AI Customer Support Platform**! This is a modern, full-stack application designed to automate customer support using AI and Retrieval-Augmented Generation (RAG). It allows users to ask questions, gets intelligent answers from your custom knowledge base, and smoothly escalates complex issues to human support agents.

---

## ✨ Features

- **🧠 Intelligent AI Chat (RAG)**: Chat with an AI that answers questions strictly based on the documents you've uploaded.
- **📚 Knowledge Base Management**: Easily upload PDF documents. The system automatically extracts the text, breaks it into chunks, and stores it in a Vector Database for lightning-fast retrieval.
- **🎫 Seamless Ticket Escalation**: If the AI isn't confident in its answer, it won't hallucinate! Instead, it politely offers the user a "Create Support Ticket" button to escalate the issue to a human agent.
- **🔐 Secure Authentication**: Full user registration, login, and secure sessions using JWT tokens.
- **📊 Admin Dashboard**: A clean dashboard to monitor metrics like total documents, total chats, total tickets, and the AI escalation rate.
- **🏗️ Clean Architecture**: Built using a strict Ports and Adapters (Hexagonal) architecture. The AI layer is completely abstracted—you can swap between Google Gemini, OpenAI, or local models with just one line of code!

---

## 🛠️ Tech Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Database**: PostgreSQL (Relational Data) & [SQLAlchemy](https://www.sqlalchemy.org/) (ORM)
- **Vector Database**: [Qdrant](https://qdrant.tech/) (For storing AI embeddings and context retrieval)
- **AI/LLM**: Google Gemini (Abstracted via Clean Architecture, making it easy to swap)

### Frontend
- **Framework**: [Next.js](https://nextjs.org/) & React (TypeScript)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **API Fetching**: Native Fetch with async/await

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing.

### 1. Prerequisites
Make sure you have the following installed:
- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js & npm](https://nodejs.org/en/)
- [Docker & Docker Compose](https://www.docker.com/) (Used to run PostgreSQL and Qdrant locally)

### 2. Set Up the Backend
1. **Navigate to the root directory**:
   ```bash
   cd "AI Customer Support Platform"
   ```
2. **Start the Databases via Docker**:
   ```bash
   docker-compose up -d
   ```
   *(This starts PostgreSQL on port 5432 and Qdrant on port 6333)*
3. **Create a Virtual Environment & Install Dependencies**:
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # On Windows
   pip install -r requirements.txt
   ```
4. **Configure Environment Variables**:
   Create a `.env` file in the root directory (you can copy `.env.example`) and add your database URLs and API keys (like `GEMINI_API_KEY`).
5. **Run Database Migrations**:
   ```bash
   alembic upgrade head
   ```
6. **Start the FastAPI Server**:
   ```bash
   uvicorn main:app --reload --reload-exclude "./frontend"
   ```
   *The backend will be running at `http://localhost:8000`*

### 3. Set Up the Frontend
1. **Navigate to the frontend folder**:
   ```bash
   cd frontend
   ```
2. **Install Node modules**:
   ```bash
   npm install
   ```
3. **Start the Next.js Development Server**:
   ```bash
   npm run dev
   ```
   *The frontend will be running at `http://localhost:3000`*

---

## 📁 Project Structure

```text
├── backend/                  
│   ├── config/               # App configuration and Environment variables
│   ├── database/             # PostgreSQL connection setup
│   ├── modules/              # Core Application Logic (Clean Architecture)
│   │   ├── ai/               # AI Ports, Adapters, and Dependencies (Gemini, Qdrant)
│   │   ├── auth/             # User registration and login
│   │   ├── chat/             # AI Conversation and Message history
│   │   ├── knowledge_base/   # PDF Uploading and chunking
│   │   └── tickets/          # Escalation ticket management
│   ├── alembic/              # Database migration scripts
│   └── main.py               # FastAPI entry point
│
├── frontend/                 
│   ├── app/                  # Next.js App Router (Pages)
│   ├── components/           # Reusable UI components (ChatInterface, etc.)
│   ├── services/             # API caller functions
│   └── types/                # TypeScript interface definitions
│
└── docker-compose.yml        # Infrastructure setup (Postgres + Qdrant)
```

---

## 🤝 How to Swap AI Models
Thanks to Clean Architecture, you are never locked into one AI provider. 
If you want to move from Gemini to OpenAI:
1. Create a new file `modules/ai/adapters/openai_adapter.py`.
2. Write a class that implements the `LLMProvider` interface.
3. Go to `modules/ai/dependencies.py` and change the return value of `get_llm_provider()` to your new OpenAI class. That's it!

---

## 📄 License
This project is for educational and portfolio purposes. Feel free to use and modify the code!
