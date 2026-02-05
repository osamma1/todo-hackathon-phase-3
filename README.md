# 🚀 Todo Hackathon Phase 3

A modern, full-stack Todo application with a stunning **Glassmorphism UI**, secure **JWT Authentication**, and a high-performance **FastAPI Backend** enhanced with **AI-Powered Chatbot**.

## 🌟 Overview

This project is a complete task management solution featuring a beautiful frontend built with Next.js and a robust backend built with FastAPI. It leverages **Better Auth** for seamless user authentication, **Neon PostgreSQL** for serverless data persistence, and **Cohere AI** for natural language task management.

---

## ✨ Features

### 🎨 Frontend (Next.js)
- **Glassmorphism UI**: Beautiful transparent cards with backdrop blur and neon glow.
- **Responsive Design**: Optimized for mobile, tablet, and desktop.
- **Animations**: Fluid transitions and micro-interactions powered by Framer Motion.
- **User Dashboard**: Visual summary of tasks and a clean task grid.
- **AI Chat Interface**: Natural language task management through an integrated chatbot.

### ⚙️ Backend (FastAPI)
- **Secure API**: JWT-based authentication with shared secrets.
- **User Isolation**: Users only see and manage their own tasks.
- **Performance**: High-speed endpoints with SQLModel for data validation.
- **CRUD Operations**: Complete task lifecycle management (Create, Read, Update, Delete).
- **AI Integration**: Cohere-powered natural language processing with tool calling.

### 🧠 AI Capabilities (Cohere)
- **Natural Language Processing**: Understand and execute commands like "Add task to buy groceries"
- **Task Operations**: Add, list, update, complete, and delete tasks via chat
- **User Information**: Query user details and task summaries through conversation
- **State Management**: Persistent conversation history in database

---

## 📂 Project Structure

```text
.
├── backend/            # FastAPI Backend
│   ├── main.py         # Entry point & CORS
│   ├── models/         # SQLModel database schemas
│   ├── api/            # API Route handlers
│   ├── agents/         # AI agent implementations
│   ├── tools/          # MCP-compatible tools for AI
│   └── Dockerfile      # Backend containerization
├── frontend/           # Next.js Frontend
│   ├── app/            # App Router (Pages & Layouts)
│   ├── components/     # Reusable UI components
│   ├── lib/api.ts      # API Client with auto-JWT
│   └── lib/chat.ts     # Chat API client
├── docker-compose.yml  # Local testing with Docker
└── README.md           # You are here!
```

---

## 🚀 Quick Start (Local Development)

### 1. Prerequisites
- Python 3.13+
- Node.js 18+
- Neon PostgreSQL Account
- Cohere API Key

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
# Create .env with COHERE_API_KEY, BETTER_AUTH_SECRET, BETTER_AUTH_URL, and DATABASE_URL
uvicorn main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
# Create .env.local with NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```

---

## 🌐 Deployment Guide

### Backend (Render.com)
1.  **Repo**: Push your code to GitHub.
2.  **Service**: Create a new **Web Service** on Render.
3.  **Config**: Select the `backend` folder as the root directory (or use the root `Dockerfile`).
4.  **Env**: Set `DATABASE_URL`, `BETTER_AUTH_SECRET`, `COHERE_API_KEY`, and `FRONTEND_URL`.

### Frontend (Vercel.com)
1.  **Repo**: Import your GitHub repository.
2.  **Settings**: Set "Next.js" as the preset and `frontend` as the root directory.
3.  **Env**: Set `NEXT_PUBLIC_API_URL` (to your Render URL) and `BETTER_AUTH_SECRET`.

---

## 🛠️ Environment Variables

### Backend (`backend/.env`)
- `DATABASE_URL`: Your Neon Postgres connection string.
- `BETTER_AUTH_SECRET`: Shared secret for JWT signing.
- `BETTER_AUTH_URL`: Your frontend URL.
- `COHERE_API_KEY`: Your Cohere API key for AI functionality.

### Frontend (`frontend/.env.local`)
- `NEXT_PUBLIC_API_URL`: Your backend API URL.
- `BETTER_AUTH_SECRET`: Same secret as backend.

---

## 🤝 Key Technologies
- **Frontend**: Next.js, Tailwind CSS, Framer Motion, Better Auth.
- **Backend**: FastAPI, SQLModel, Uvicorn, PyJWT.
- **AI**: Cohere API for natural language processing.
- **Infrastructure**: Neon Postgres, Render, Vercel.

---

*Built with ❤️ for the Todo Hackathon.*