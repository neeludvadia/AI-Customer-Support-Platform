# AI Customer Support Platform 🤖💼

Welcome to the **AI Customer Support Platform**! This is a modern, enterprise-grade full-stack application designed to automate customer support using AI and Retrieval-Augmented Generation (RAG). 

It allows users to ask questions, gets intelligent answers grounded strictly in your custom knowledge base, and smoothly escalates complex issues to human support agents.

---

## ✨ Key Features

- **🧠 Intelligent AI Chat (RAG)**: Chat with an AI that answers questions strictly based on the documents you've uploaded, eliminating hallucinations.
- **📚 Knowledge Base Management**: Upload PDF documents. The system automatically extracts text, chunks it, embeds it, and stores it in Qdrant for lightning-fast semantic retrieval.
- **🎫 Seamless Ticket Escalation**: If the AI isn't confident, it politely offers the user a "Create Support Ticket" button to escalate the issue to a human agent.
- **🔐 Secure Authentication (Token Rotation)**: Highly secure session management using short-lived JWT Access Tokens and long-lived Refresh Tokens stored in HttpOnly cookies, complete with token rotation and device tracking to thwart replay attacks.
- **📊 Admin Dashboard**: A clean dashboard to monitor metrics like total documents, total chats, total tickets, and system health status.
- **🏗️ Clean Architecture**: Built using a strict Ports and Adapters (Hexagonal) architecture on the backend. The AI layer is completely abstracted—you can swap between Google Gemini, OpenAI, or local models easily.

---

## 🏗️ Architecture Deep Dive

The platform is divided into two decoupled layers: the Next.js Frontend and the FastAPI Backend.

### 1. Backend Architecture (Hexagonal / Ports & Adapters)
The backend enforces a strict separation of concerns to keep business logic independent of external frameworks and databases.

* **Domain / Models**: SQLAlchemy models define the database schema (e.g., `User`, `Ticket`, `Message`, `RefreshToken`).
* **Repositories**: Data access layers that handle all SQL queries. Business logic never touches the database directly; it relies on repository methods.
* **Services**: The core business logic. This layer processes data, enforces rules, and orchestrates actions (e.g., `AuthService` handles hashing and token rotation).
* **Routers / Controllers**: FastAPI endpoints that handle HTTP requests, validate input using Pydantic DTOs, and route them to the appropriate Services.
* **Adapters**: The AI module uses adapters for LLM providers (e.g., Gemini) and Vector DBs (e.g., Qdrant). This means the core chat logic talks to an `LLMProvider` interface, completely unaware of whether it's using Google or OpenAI under the hood.

### 2. Frontend Architecture (Next.js App Router)
The frontend is built for extreme performance, strong typing, and modularity using Next.js 14+ and React.

* **App Router (`app/`)**: Utilizes the modern Next.js App Router for server-centric routing. Layouts (`layout.tsx`) wrap pages (`page.tsx`) to prevent redundant re-renders of the sidebar and navigation.
* **Server & Client Components**: Pages default to React Server Components (RSC) for zero-bundle-size performance. Interactive components (like the chat input or dashboard charts) are explicitly marked with `"use client"`.
* **Tailwind CSS Styling**: Utility-first styling is used globally. A centralized `globals.css` defines core CSS variables, while Tailwind handles responsive design and dark/light modes.
* **Type-Safe API Contracts (`types/`)**: TypeScript interfaces in the `types/` folder strictly mirror the backend's Pydantic schemas, ensuring complete type safety from database to DOM.
* **Service-Oriented Fetching (`services/`)**: Components never call `fetch` directly. Instead, they call modular service singletons (e.g., `ticketService.getTickets()`), which keeps UI components clean and makes API mocking easy.

### 3. Authentication Flow (Refresh Token Rotation)
Authentication is built to enterprise security standards:
1. **Login**: User submits credentials. Backend verifies and issues an Access Token (15 mins) and a Refresh Token (7 days).
2. **Storage**: Both tokens are sent to the browser as **HttpOnly, SameSite=Lax** cookies, making them immune to XSS attacks. The Refresh Token is hashed (SHA-256) and saved in PostgreSQL alongside device info.
3. **Session Healing**: The frontend uses a global `fetchWithAuth` interceptor. If any API call returns `401 Unauthorized`, the interceptor pauses the app, hits `/auth/refresh`, rotates the tokens (invalidating the old refresh token to prevent replay attacks), and seamlessly retries the original request.
4. **Edge Middleware Protection**: Next.js Edge Middleware (`middleware.ts`) intercepts requests to protected routes (`/dashboard`) and instantly redirects unauthenticated users to `/login` with zero layout shift.

### 4. RAG Pipeline (Retrieval-Augmented Generation)
1. **Ingestion**: Admin uploads a PDF. 
2. **Processing**: The backend extracts text and uses Recursive Character Text Splitting to break it into semantic chunks.
3. **Embedding**: Chunks are embedded using an embedding model (e.g., Gemini Embeddings) and stored in Qdrant with payload metadata.
4. **Retrieval**: When a user asks a question, the query is embedded, and Qdrant performs a Cosine Similarity search to find the most relevant document chunks.
5. **Generation**: The retrieved chunks are injected into the LLM system prompt as ground truth context, forcing the LLM to answer *only* using the provided data.

---

## 🛠️ Tech Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Database**: PostgreSQL (Relational Data) & [SQLAlchemy](https://www.sqlalchemy.org/) (ORM)
- **Vector Database**: [Qdrant](https://qdrant.tech/) 
- **AI/LLM**: Google Gemini (Abstracted via Clean Architecture)

### Frontend
- **Framework**: [Next.js](https://nextjs.org/) App Router & React (TypeScript)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **API Fetching**: Native Fetch with custom `fetchWithAuth` Interceptor

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### 1. Prerequisites
- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js & npm](https://nodejs.org/en/)
- [Docker & Docker Compose](https://www.docker.com/)

### 2. Set Up the Backend
1. **Navigate to the root directory**:
   ```bash
   cd "AI Customer Support Platform"
   ```
2. **Start the Databases via Docker**:
   ```bash
   docker-compose up -d
   ```
   *(Starts PostgreSQL on port 5433 and Qdrant on port 6333)*
3. **Create a Virtual Environment & Install Dependencies**:
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # On Windows
   pip install -r requirements.txt
   ```
4. **Configure Environment Variables**:
   Create a `.env` file in the root directory (copy `.env.example`) and add your database URLs and API keys (like `GEMINI_API_KEY`).
5. **Run Database Migrations**:
   ```bash
   alembic upgrade head
   ```
6. **Start the FastAPI Server**:
   ```bash
   uvicorn main:app --reload --reload-exclude "./frontend" --host 127.0.0.1 --port 3456
   ```
   *The backend will run at `http://127.0.0.1:3456`*

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
   *The frontend will run at `http://localhost:3000`*

---

## 📁 Project Structure

```text
├── config/                   # App configuration and Environment variables
├── database/                 # PostgreSQL connection setup
├── modules/                  # Core Application Logic (Clean Architecture)
│   ├── admin/                # Admin Dashboard endpoints and metrics
│   ├── ai/                   # AI Ports, Adapters, and Dependencies (Gemini, Qdrant)
│   ├── auth/                 # Auth logic, JWT issuance, Refresh Token Rotation
│   ├── chat/                 # AI Conversation and Message history orchestration
│   ├── knowledge_base/       # PDF Uploading, text extraction, and chunking
│   └── tickets/              # Escalation ticket management and CRUD
├── alembic/                  # Database migration scripts
├── main.py                   # FastAPI entry point
│
├── frontend/                 
│   ├── app/                  # Next.js App Router (Pages & Layouts)
│   ├── components/           # Reusable UI components (Dashboard, ChatInterface)
│   ├── services/             # API caller functions (Explicit fetches with headers)
│   ├── utils/                # Utilities like fetchWithAuth interceptor
│   ├── middleware.ts         # Edge route protection for authenticated pages
│   └── types/                # TypeScript interface definitions for Pydantic alignment
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
